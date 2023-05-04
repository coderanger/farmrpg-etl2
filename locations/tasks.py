import structlog
from asgiref.sync import sync_to_async

from utils.http import client

from .models import Location, LocationItem
from .parser import parse_location, parse_locations
from .serializers import LocationHTMLSerializer

log = structlog.stdlib.get_logger(mod="locations.tasks")


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
    log.debug("Scraping locations from HTML")
    resp = await client.get("/locations.php")
    resp.raise_for_status()
    for loc_type, loc_id in parse_locations(resp.content):
        await scrape_from_html(loc_type, loc_id)
    log.info("Finished scraping locations from HTML")
