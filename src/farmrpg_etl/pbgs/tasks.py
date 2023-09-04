import structlog

from ..items.models import Item
from ..utils.http import client

from .models import ProfileBackground
from .parsers import parse_gallery

log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_html():
    resp = await client.get("/gallery.php")
    resp.raise_for_status()

    for parsed in parse_gallery(resp.content):
        data = {}
        if parsed.id is not None:
            data["game_id"] = parsed.id

        if "/light/" in parsed.image:
            data["light_image"] = parsed.image
            data["dark_image"] = parsed.image.replace("/light/", "/dark/")
        else:
            data["light_image"] = parsed.image.replace("/dark/", "/light/")
            data["dark_image"] = parsed.image

        if parsed.cost_item == "Silver":
            data["cost_silver"] = parsed.cost_quantity
        elif parsed.cost_item == "Gold":
            data["cost_gold"] = parsed.cost_quantity
        elif parsed.cost_item is not None:
            data["cost_item_id"] = await Item.objects.values_list("id", flat=True).aget(
                name=parsed.cost_item
            )
            data["cost_item_quantity"] = parsed.cost_quantity

        await ProfileBackground.objects.aupdate_or_create(
            name=parsed.name, defaults=data
        )
