import datetime
from zoneinfo import ZoneInfo
import structlog

from utils.http import client

from .models import BorgenItem
from .parsers import parse_borgens

SERVER_TIME = ZoneInfo("America/Chicago")


log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_html():
    resp = await client.get("/tent.php")
    resp.raise_for_status()

    today = datetime.datetime.now(tz=SERVER_TIME).date()
    for parsed_item in parse_borgens(resp.content):
        await BorgenItem.objects.aupdate_or_create(
            date=today,
            item_id=parsed_item.item,
            defaults={"price": parsed_item.price}
            if parsed_item.price is not None
            else {},
        )
