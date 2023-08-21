import collections
import os

import httpx
import sentry_sdk
import structlog
from asgiref.sync import sync_to_async

from cron.decorators import cron
from utils.http import client

from .models import Item, LocksmithItem, RecipeItem, WishingWellItem
from .parsers import parse_item
from .serializers import ItemAPISerializer

log = structlog.stdlib.get_logger(mod="items.tasks")

# All this fuss is because there are some unreleased items so there are gaps in
# valid IDs. There hasn't (yet) been a gap bigger than 20 but this may need to be
# increased over time.
MAX_ITEM_ID_GAP = 20

# ID of the wishing well spreadsheet.
WISHING_WELL_SPREADSHEET_ID = "1hYP-_PkvKvIm0hz8nhLhqzzZhAYl0zY6aRDoi6oN5qQ"

# An HTTP client without the game cookies.
WISHING_WELL_CLIENT = httpx.AsyncClient()


class ItemNotFound(Exception):
    """A stubby exception used in the scrape tasks."""


async def scrape_from_api(item_id: int):
    resp = await client.get(f"/api/item/{item_id}")
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ItemNotFound
    item = await Item.objects.filter(id=data[0]["id"]).afirst()
    ser = ItemAPISerializer(instance=item, data=data[0])
    await sync_to_async(ser.is_valid)(raise_exception=True)
    await sync_to_async(ser.save)()


async def scrape_from_html(item_id: int):
    resp = await client.get("/item.php", params={"id": item_id})
    resp.raise_for_status()
    parsed = parse_item(resp.content)

    await Item.objects.filter(id=item_id).aupdate(
        flea_market_price=parsed.flea_market_price,
        from_event=parsed.from_event,
    )

    seen_recipe_ids = []
    for parsed_recipe in parsed.recipe:
        recipe, _ = await RecipeItem.objects.aupdate_or_create(
            item_id=item_id,
            ingredient_item_id=parsed_recipe.id,
            defaults={"quantity": parsed_recipe.quantity},
        )
        seen_recipe_ids.append(recipe.id)
    await RecipeItem.objects.filter(item_id=item_id).exclude(
        id__in=seen_recipe_ids
    ).adelete()

    item = await Item.objects.only("locksmith_grab_bag").filter(id=item_id).afirst()
    assert item is not None
    if not item.locksmith_grab_bag:
        seen_locksmith_id = []
        for parsed_locksmith in parsed.locksmith:
            if parsed_locksmith.gold:
                await Item.objects.filter(id=item_id).aupdate(
                    locksmith_gold=parsed_locksmith.quantity
                )
            else:
                locksmith, _ = await LocksmithItem.objects.aupdate_or_create(
                    item_id=item_id,
                    output_item_id=parsed_locksmith.id,
                    defaults={
                        "quantity_min": parsed_locksmith.quantity,
                        "quantity_max": parsed_locksmith.quantity,
                    },
                )
                seen_locksmith_id.append(locksmith.id)
        await LocksmithItem.objects.filter(item_id=item_id).exclude(
            id__in=seen_locksmith_id
        ).adelete()


async def scrape_recipes():
    log.info("Scraping recipes")
    resp = await client.get("/api/recipes")
    resp.raise_for_status()
    data = resp.json()
    seen_recipe_item_ids = []
    seen_locksmith_item_ids = []
    for row in data:
        item = await Item.objects.filter(id=row["item_id"]).afirst()
        if item is None:
            msg = f"Got item ID {row['item_id']} from recipe that does not exist"
            log.error(msg)
            sentry_sdk.capture_message(msg)
            continue
        if not item.can_craft ^ item.can_cook ^ item.can_locksmith:
            msg = f"Item {item.id} has bad recipe can_* flags"
            log.error(msg)
            sentry_sdk.capture_message(msg)
            continue
        if item.can_craft or item.can_cook:
            # Simple case, this is a recipe.
            recipe_item, _ = await RecipeItem.objects.aupdate_or_create(
                item=item,
                ingredient_item_id=row["req_id"],
                defaults={"quantity": row["req_amt"]},
            )
            seen_recipe_item_ids.append(recipe_item.id)
        elif item.can_locksmith:
            # Slightly more complex, this is an openable.
            quantity_min = quantity_max = row["req_amt"]
            if item.locksmith_grab_bag:
                if row["req_amt"] <= 10:
                    quantity_min = 1
                else:
                    quantity_min = 10
            locksmith_item, _ = await LocksmithItem.objects.aupdate_or_create(
                item=item,
                output_item_id=row["req_id"],
                defaults={"quantity_min": quantity_min, "quantity_max": quantity_max},
            )
            seen_locksmith_item_ids.append(locksmith_item.id)
    await RecipeItem.objects.exclude(id__in=seen_recipe_item_ids).adelete()
    await LocksmithItem.objects.exclude(id__in=seen_locksmith_item_ids).adelete()


@cron("H/30 * * * * H", name="scrape_items")
async def scrape_all():
    cur_id = 10  # Start at 10 because 1-9 are unused.
    missing = 0
    while True:
        log.debug("Scraping item", id=cur_id)
        try:
            await scrape_from_api(cur_id)
            missing = 0  # It worked so reset the count.
            # await scrape_from_html(cur_id)
        except ItemNotFound:
            missing += 1
            if missing >= MAX_ITEM_ID_GAP:
                break
        except Exception as exc:
            # Keep going for future items.
            sentry_sdk.capture_exception(exc)
            log.exception("Error scraping item")
        cur_id += 1
    await scrape_recipes()


@cron("@hourly", name="scrape_wishing_well")
async def scrape_wishing_well_from_sheets():
    # Download and format the Wishing Well data from the spreadsheet.
    resp = await WISHING_WELL_CLIENT.get(
        f"https://sheets.googleapis.com/v4/spreadsheets/{WISHING_WELL_SPREADSHEET_ID}/values/B5:C",
        params={"key": os.environ["GOOGLE_SHEETS_API_KEY"]},
        timeout=30,
    )
    resp.raise_for_status()
    page = resp.json()
    rows = page["values"]
    headers = rows.pop(0)
    # Sanity check just in case.
    assert headers == ["Input", "Output"]
    ww_drops = collections.defaultdict(list)
    all_items = set()
    for row in rows:
        ww_drops[row[0]].append(row[1])
        all_items.add(row[0])
        all_items.add(row[1])
    # Grab item ID from the DB.
    item_ids = {
        item["name"]: item["id"]
        async for item in Item.objects.filter(name__in=all_items).values("id", "name")
    }
    # Update database.
    seen_ids = []
    for input, outputs in ww_drops.items():
        for output in outputs:
            ww, _ = await WishingWellItem.objects.aupdate_or_create(
                input_item_id=item_ids[input],
                output_item_id=item_ids[output],
                defaults={"chance": 1 / len(outputs)},
            )
            seen_ids.append(ww.id)
    await WishingWellItem.objects.exclude(id__in=seen_ids).adelete()
