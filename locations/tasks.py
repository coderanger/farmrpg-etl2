import time

import structlog
from asgiref.sync import sync_to_async
from django.db.models import Prefetch

from items.models import Item
from utils.http import client

from .drop_simulator import simulate_drops
from .models import DropRates, DropRatesItem, Location, LocationItem
from .parser import parse_location, parse_locations
from .serializers import LocationHTMLSerializer

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
    "Potato Seeds": ["Potato", "Gold Potato"],
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

MANUAL_FISHING_ONLY = {
    "Gold Catfish",
    "Gold Coral",
    "Gold Drum",
    "Gold Flier",
    "Gold Jelly",
    "Gold Sea Bass",
    "Gold Sea Crest",
    "Gold Trout",
    "Goldfin",
    "Goldgill",
    "Goldjack",
    "Goldray",
}


async def scrape_from_html(loc_type: str, loc_id: int):
    log.debug("Scraping location from HTML", type=loc_type, id=loc_id)
    resp = await client.get(
        "/location.php", params={"type": loc_type, "id": str(loc_id)}
    )
    resp.raise_for_status()
    data = parse_location(resp.content)
    data["type"] = loc_type
    data["game_id"] = loc_id

    try:
        items = data.pop("items")
        loc = await Location.objects.filter(type=loc_type, game_id=loc_id).afirst()
        ser = LocationHTMLSerializer(instance=loc, data=data)
        await sync_to_async(lambda: ser.is_valid(raise_exception=True))()
        loc: Location = await sync_to_async(ser.save)()

        for item_id in items:
            await LocationItem.objects.aupdate_or_create(
                location=loc,
                item_id=item_id,
            )
        await LocationItem.objects.filter(location=loc).exclude(
            item_id__in=items
        ).adelete()
    except Exception:
        log.exception("Error loading location", type=loc_type, id=loc_id)


async def scrape_all_from_html():
    resp = await client.get("/locations.php")
    resp.raise_for_status()
    for loc_type, loc_id in parse_locations(resp.content):
        await scrape_from_html(loc_type, loc_id)
        await update_drop_rates_for_location(loc_type, loc_id)


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
            # Normal.
            (
                {"manual_fishing": False, "runecube": False},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.all()
                    if it.item.name not in MANUAL_FISHING_ONLY
                },
            ),
            # Manual fishing.
            (
                {"manual_fishing": True, "runecube": False},
                {
                    it.item.id: it.item.reg_weight
                    async for it in location.location_items.all()
                },
            ),
            # Runecube.
            (
                {"runecube": True, "manual_fishing": False},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.all()
                    if it.item.name not in MANUAL_FISHING_ONLY
                },
            ),
            # Runecube + manual fishing.
            (
                {"runecube": True, "manual_fishing": True},
                {
                    it.item.id: it.item.runecube_weight
                    async for it in location.location_items.all()
                },
            ),
        ]
    else:
        raise ValueError(f"Unknown drops_for {drops_for!r}")

    for variant_flags, variant_items in variants:
        rates, _ = await DropRates.objects.aget_or_create(
            location=location, seed=seed, **variant_flags
        )
        new_hash = hash(tuple(variant_items.items()))
        # Check the hash to see if an update is needed.
        if (not force) and new_hash == rates.hash:
            # All good!
            continue

        # Spawn a drop sim in a background thread. It will spend most of its time in numpy
        # C land with the GIL released.
        log.debug(
            "Starting drop sim", location=location, seed=seed, flags=variant_flags
        )
        start_ts = time.monotonic()
        drops, total_drops = await sync_to_async(
            simulate_drops, thread_sensitive=False
        )(variant_items)
        end_ts = time.monotonic()
        sim_tim = end_ts - start_ts
        log.debug(
            "Finished drop sim",
            location=location,
            seed=seed,
            flags=variant_flags,
            seconds=sim_tim,
        )
        for item_id, item_drops in drops.items():
            base_drop_rate = 1
            if location is not None and location.base_drop_rate is not None:
                base_drop_rate = location.base_drop_rate
            rate = (total_drops / base_drop_rate) / item_drops
            await DropRatesItem.objects.aupdate_or_create(
                drop_rates=rates, item_id=item_id, defaults={"rate": rate}
            )
        await DropRates.objects.filter(pk=rates.pk).aupdate(
            hash=new_hash, compute_time=sim_tim
        )
        await DropRatesItem.objects.filter(drop_rates=rates).exclude(
            item_id__in=variant_items
        ).adelete()


async def update_crop_drop_rates():
    for seed_name in SEEDS.keys():
        seed = await Item.objects.aget(name=seed_name)
        await update_drop_rates_for(seed)
