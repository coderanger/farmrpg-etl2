import collections
import os
import httpx
import structlog
from asgiref.sync import sync_to_async

from utils.http import client

from .models import Item, WishingWellItem
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
    log.debug("Scraping item from API", id=item_id)
    resp = await client.get(f"/api/item/{item_id}")
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ItemNotFound
    item = await Item.objects.filter(id=data[0]["id"]).afirst()
    ser = ItemAPISerializer(instance=item, data=data[0])
    await sync_to_async(lambda: ser.is_valid(raise_exception=True))()
    await sync_to_async(ser.save)()


async def scrape_all_from_api():
    cur_id = 10  # Start at 10 because 1-9 are unused.
    missing = 0
    while True:
        try:
            await scrape_from_api(cur_id)
            missing = 0  # It worked so reset the count.
        except ItemNotFound:
            missing += 1
            if missing >= MAX_ITEM_ID_GAP:
                break
        cur_id += 1


async def scrape_wishing_well_from_sheets():
    log.debug("Scraping wishing well from Sheet")
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
    log.debug("Finished scraping wishing well from Sheet")
