import structlog
from asgiref.sync import sync_to_async

from utils.http import client

from .models import Item
from .serializers import ItemAPISerializer

log = structlog.stdlib.get_logger(mod="items.tasks")

# All this fuss is because there are some unreleased items so there are gaps in
# valid IDs. There hasn't (yet) been a gap bigger than 20 but this may need to be
# increased over time.
MAX_ITEM_ID_GAP = 20


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
