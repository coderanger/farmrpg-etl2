import datetime
from zoneinfo import ZoneInfo

import structlog

from items.models import Item
from utils.http import client

from .models import CommunityCenter
from .parsers import parse_community_center

SERVER_TIME = ZoneInfo("America/Chicago")


log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_html():
    today = datetime.datetime.now(tz=SERVER_TIME).date()

    resp = await client.get("/comm.php")
    resp.raise_for_status()
    for parsed in parse_community_center(resp.content, today=today):
        input_item_id = parsed.input_item
        if input_item_id is None:
            input_item_id = await Item.objects.values_list("id", flat=True).aget(
                name=parsed.input_item_name
            )

        await CommunityCenter.objects.aupdate_or_create(
            date=parsed.date,
            defaults={
                "input_item_id": input_item_id,
                "input_quantity": parsed.input_quantity,
                "output_item_id": parsed.output_item,
                "output_quantity": parsed.output_quantity,
                "progress": parsed.progress,
            },
        )
