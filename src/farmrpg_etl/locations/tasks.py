import time

import sentry_sdk
import structlog
from asgiref.sync import sync_to_async
from django.db.models import Prefetch

from ..cron.decorators import cron
from ..items.models import Item
from ..utils.http import client
from .drop_simulator import simulate_drops
from .models import DropRates, DropRatesItem, Location, LocationItem

log = structlog.stdlib.get_logger(mod=__name__)


SEEDS = {
    "Pepper Seeds": ["Peppers", "Gold Peppers"],
    "Carrot Seeds": ["Carrot", "Gold Carrot", "Runestone 01"],
    "Pea Seeds": ["Peas", "Gold Peas"],
    "Cucumber Seeds": ["Cucumber", "Gold Cucumber", "Runestone 06"],
    "Eggplant Seeds": ["Eggplant", "Gold Eggplant", "Runestone 20"],
    "Radish Seeds": ["Radish", "Runestone 07"],
    "Onion Seeds": ["Onion"],
    "Hops Seeds": ["Hops", "Runestone 16"],
    "Potato Seeds": ["Potato", "Gold Potato", "Hot Potato"],
    "Tomato Seeds": ["Tomato", "Winged Amulet"],
    "Leek Seeds": ["Leek", "Runestone 10"],
    "Watermelon Seeds": ["Watermelon", "Piece of Heart"],
    "Corn Seeds": ["Corn", "Runestone 11", "Popcorn"],
    "Cabbage Seeds": ["Cabbage"],
    "Pine Seeds": ["Pine Tree"],
    "Pumpkin Seeds": ["Pumpkin"],
    "Wheat Seeds": ["Wheat"],
    "Mushroom Spores": ["Mushroom"],
    "Broccoli Seeds": ["Broccoli"],
    "Cotton Seeds": ["Cotton"],
    "Sunflower Seeds": ["Sunflower"],
    "Beet Seeds": ["Beet"],
    "Rice Seeds": ["Rice"],
}

API_KEY_TO_TYPE = {
    "explore_locations": "explore",
    "fishing_locations": "fishing",
    "mining_locations": "mining",
}


async def _ingest_location_items(
    loc: Location,
    output_ids: list[int],
    item_ids: str | None,
    sometimes: bool = False,
    frozen: bool = False,
    mining_level: int | None = None,
):
    if not item_ids:
        return
    for item_id in item_ids.split(","):
        try:
            loc_item, _ = await LocationItem.objects.aupdate_or_create(
                location=loc,
                item_id=int(item_id.strip()),
                defaults={
                    "sometimes": sometimes,
                    "frozen": frozen,
                    "mining_level": mining_level,
                },
            )
            output_ids.append(loc_item.pk)
        except Exception as exc:
            # Probably an item that isn't ingested yet. Just move on.
            log.exception("Error updating location item", loc=loc.name, item=item_id)
            sentry_sdk.capture_exception(exc)


@cron("@hourly")
async def scrape_locations():
    resp = await client.get("/api.php", params={"method": "location"})
    resp.raise_for_status()

    # TODO: Compute base drop rates from explore_texts.
    data = resp.json()
    for api_key, loc_type in API_KEY_TO_TYPE.items():
        for loc_data in data[api_key]:
            if (
                ("active" in loc_data and loc_data["active"] != 1)
                or (loc_type == Location.TYPE_EXPLORE and loc_data["special"])
                or (
                    loc_data == Location.TYPE_MINING
                    and (loc_data["mine"] != 1 or loc_data["staff_only"] != 0)
                )
            ):
                continue
            # Special case for Sinking Swamp being both an exploring an fishing location, rename one of them.
            if loc_type == "explore" and loc_data.get("name") == "Sinking Swamp":
                loc_data["name"] = "Sinking Swamp Exploring"
            log.info("Ingesting location", loc=loc_data.get("name"))
            mining_data = {}
            if loc_type == Location.TYPE_MINING:
                mining_data["mining_pickaxe"] = await Item.objects.filter(
                    name=loc_data["req_pickaxe"]
                ).afirst()
                # These are FKs upstream so we don't need to re-validate in theory.
                mining_data["mining_charm_id"] = int(loc_data["drop_effect_item_id"])
                mining_data["mining_lantern_id"] = int(
                    loc_data["autoexcavation_save_item_id"]
                )
            loc, _ = await Location.objects.aupdate_or_create(
                game_id=loc_data["id"],
                type=loc_type,
                defaults={
                    "name": loc_data["name"],
                    "image": loc_data["img"],
                    **mining_data,
                },
            )
            item_ids = []
            if loc_type == Location.TYPE_EXPLORE:
                await _ingest_location_items(
                    loc,
                    item_ids,
                    loc_data["possible_items"],
                )
            elif loc_type == Location.TYPE_FISHING:
                await _ingest_location_items(
                    loc,
                    item_ids,
                    loc_data["possible_fish"],
                )
                await _ingest_location_items(
                    loc,
                    item_ids,
                    loc_data["event_dec_possible_fish"],
                    frozen=True,
                )
            elif loc_type == Location.TYPE_MINING:
                # Upstream the items are stored with all the duplicates so sort them out here.
                level_1 = {i.strip() for i in loc_data["possible_items9"].split(",")}
                level_10 = {
                    i.strip() for i in loc_data["possible_items99"].split(",")
                } - level_1
                level_100 = (
                    {i.strip() for i in loc_data["possible_items999"].split(",")}
                    - level_10
                    - level_1
                )
                level_1000 = (
                    {i.strip() for i in loc_data["possible_items9999"].split(",")}
                    - level_100
                    - level_10
                    - level_1
                )
                level_10000 = (
                    {i.strip() for i in loc_data["possible_items99999"].split(",")}
                    - level_1000
                    - level_100
                    - level_10
                    - level_1
                )
                await _ingest_location_items(
                    loc,
                    item_ids,
                    ",".join(level_1),
                    mining_level=1,
                )
                await _ingest_location_items(
                    loc,
                    item_ids,
                    ",".join(level_10),
                    mining_level=10,
                )
                await _ingest_location_items(
                    loc,
                    item_ids,
                    ",".join(level_100),
                    mining_level=100,
                )
                await _ingest_location_items(
                    loc,
                    item_ids,
                    ",".join(level_1000),
                    mining_level=1000,
                )
                await _ingest_location_items(
                    loc,
                    item_ids,
                    ",".join(level_10000),
                    mining_level=10000,
                )
                # Process the deposits data which are special.
                for val in loc_data["possible_deposits"].split(","):
                    deposit_parts = val.split("|")
                    deposit_item_id = int(deposit_parts[0].strip())
                    deposit_quantity = int(deposit_parts[1].strip())
                    loc_item, _ = await LocationItem.objects.aupdate_or_create(
                        location=loc,
                        item_id=deposit_item_id,
                        defaults={
                            "mining_deposit_quantity": deposit_quantity,
                        },
                    )
                    item_ids.append(loc_item.pk)
            await (
                LocationItem.objects.filter(location=loc)
                .exclude(pk__in=item_ids)
                .adelete()
            )
            try:
                await update_drop_rates_for_location(loc_type, loc.game_id)
            except Exception as exc:
                log.exception("Error updating drop rates", loc=loc.name)
                sentry_sdk.capture_exception(exc)


async def update_drop_rates_for_location(
    loc_type: str, loc_id: int, force: bool = False
):
    loc = (
        await Location.objects.filter(type=loc_type, game_id=loc_id)
        .prefetch_related(
            Prefetch(
                "location_items",
                queryset=LocationItem.objects.all().select_related("item"),
            )
        )
        .aget()
    )
    await update_drop_rates_for(loc)


async def update_drop_rates_for(drops_for: Location | Item, force: bool = False):
    if isinstance(drops_for, Item):
        location = None
        seed = drops_for
        seed_items = [await Item.objects.aget(name=name) for name in SEEDS[seed.name]]
        variants = [
            # Normal.
            ({"runecube": False}, {it.id: it.reg_weight for it in seed_items}),
            # Runecube.
            ({"runecube": True}, {it.id: it.runecube_weight for it in seed_items}),
        ]
    elif drops_for.type == Location.TYPE_EXPLORE:
        location = drops_for
        seed = None
        variants = [
            # Normal, no perks.
            (
                {"iron_depot": False, "runecube": False},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.all()
                },
            ),
            # Iron depot.
            (
                {"iron_depot": True, "runecube": False},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.all()
                    if it.item.name != "Iron" and it.item.name != "Nails"
                },
            ),
            # Runecube.
            (
                {"runecube": True, "iron_depot": False},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.all()
                },
            ),
            # Runecube + iron depot.
            (
                {"runecube": True, "iron_depot": True},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.all()
                    if it.item.name != "Iron" and it.item.name != "Nails"
                },
            ),
        ]
    elif drops_for.type == Location.TYPE_FISHING:
        location = drops_for
        seed = None
        variants = [
            # UNFROZEN
            # Normal.
            (
                {"manual_fishing": False, "runecube": False, "frozen": False},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.filter(frozen=False)
                    if not it.item.manual_fishing_only
                },
            ),
            # Manual fishing.
            (
                {"manual_fishing": True, "runecube": False, "frozen": False},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.filter(frozen=False)
                },
            ),
            # Runecube.
            (
                {"runecube": True, "manual_fishing": False, "frozen": False},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.filter(frozen=False)
                    if not it.item.manual_fishing_only
                },
            ),
            # Runecube + manual fishing.
            (
                {"runecube": True, "manual_fishing": True, "frozen": False},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.filter(frozen=False)
                },
            ),
            # FROZEN
            # Normal.
            (
                {"manual_fishing": False, "runecube": False, "frozen": True},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.all()
                    if not it.item.manual_fishing_only
                },
            ),
            # Manual fishing.
            (
                {"manual_fishing": True, "runecube": False, "frozen": True},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.all()
                },
            ),
            # Runecube.
            (
                {"runecube": True, "manual_fishing": False, "frozen": True},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.all()
                    if not it.item.manual_fishing_only
                },
            ),
            # Runecube + manual fishing.
            (
                {"runecube": True, "manual_fishing": True, "frozen": True},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.all()
                },
            ),
            # FROZEN ONLY
            # Normal.
            (
                {"runecube": False, "frozen_only": True},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.filter(frozen=True)
                    if not it.item.manual_fishing_only
                },
            ),
            # Runecube.
            (
                {"runecube": True, "frozen_only": True},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.filter(frozen=True)
                    if not it.item.manual_fishing_only
                },
            ),
        ]
    elif drops_for.type == Location.TYPE_MINING:
        # TODO.
        location = drops_for
        seed = None
        variants = []
    else:
        raise ValueError(f"Unknown drops_for {drops_for!r}")

    seen_rates = []
    for variant_flags, variant_items in variants:
        if not variant_items:
            raise ValueError(
                f"Trying to generate drops for {drops_for.name} but got no "
                f"items: {variant_flags!r}"
            )
        rates, _ = await DropRates.objects.aget_or_create(
            location=location, seed=seed, **variant_flags
        )
        seen_rates.append(rates.pk)
        new_hash = hash(tuple(sorted(variant_items.items())))
        # Check the hash to see if an update is needed.
        if (not force) and new_hash == rates.hash:
            # All good!
            continue

        # Spawn a drop sim in a background thread. It will spend most of its time in
        # numpy C land with the GIL released.
        log.debug(
            "Starting drop sim",
            location=location.name if location else location,
            seed=seed.name if seed else seed,
            flags=variant_flags,
            old_hash=rates.hash,
            new_hash=new_hash,
        )
        start_ts = time.monotonic()
        drops, total_drops = await sync_to_async(
            simulate_drops, thread_sensitive=False
        )(variant_items)
        end_ts = time.monotonic()
        sim_tim = end_ts - start_ts
        log.debug(
            "Finished drop sim",
            location=location.name if location else location,
            seed=seed.name if seed else seed,
            flags=variant_flags,
            seconds=sim_tim,
        )
        silver_per_hit = xp_per_hit = 0
        for item_id, item_drops in drops.items():
            base_drop_rate = 1
            if location is not None and location.base_drop_rate is not None:
                base_drop_rate = location.base_drop_rate
            rate = (total_drops / base_drop_rate) / item_drops
            item_silver, item_xp = await Item.objects.values_list(
                "sell_price", "xp"
            ).aget(id=item_id)
            silver_per_hit += item_silver / rate
            xp_per_hit += item_xp / rate
            await DropRatesItem.objects.aupdate_or_create(
                drop_rates=rates, item_id=item_id, defaults={"rate": rate}
            )
        await DropRates.objects.filter(pk=rates.pk).aupdate(
            hash=new_hash,
            compute_time=sim_tim,
            silver_per_hit=silver_per_hit,
            xp_per_hit=xp_per_hit,
        )
        await (
            DropRatesItem.objects.filter(drop_rates=rates)
            .exclude(item_id__in=variant_items)
            .adelete()
        )

    #     rates2, _ = await DropRates.objects.aget_or_create(
    #         location=location, seed=seed, **variant_flags
    #     )
    #     if rates2.hash is None:
    #         raise Exception("boom")
    await (
        DropRates.objects.filter(location=location, seed=seed)
        .exclude(pk__in=seen_rates)
        .adelete()
    )


@cron("@hourly")
async def update_crop_drop_rates():
    for seed_name in SEEDS.keys():
        seed = await Item.objects.aget(name=seed_name)
        await update_drop_rates_for(seed)
