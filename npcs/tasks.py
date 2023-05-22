import structlog

from items.models import Item
from utils.http import client

from .models import NPC, NPCItem
from .parsers import parse_manage_npc

log = structlog.stdlib.get_logger(mod=__name__)


async def _update_items(npc: NPC, relationship: str, item_names: list[str]):
    seen_item_ids = []
    for item_name in item_names:
        item_id = (
            await Item.objects.filter(name=item_name)
            .values_list("id", flat=True)
            .aget()
        )
        await NPCItem.objects.aupdate_or_create(
            npc=npc, item_id=item_id, defaults={"relationship": relationship}
        )
        seen_item_ids.append(item_id)
    await NPCItem.objects.filter(npc=npc, relationship=relationship).exclude(
        item_id__in=seen_item_ids
    ).adelete()


async def scrape_all_from_html():
    resp = await client.get("/manage_npc.php")
    resp.raise_for_status()
    for data in parse_manage_npc(resp.content):
        log.debug("Updating NPC", id=data.get("id"), name=data.get("name"))
        npc, _ = await NPC.objects.aupdate_or_create(
            id=data["id"], defaults={"name": data["name"], "image": data["image"]}
        )
        await _update_items(npc, "loves", data["loves"])
        await _update_items(npc, "likes", data["likes"])
        await _update_items(npc, "hates", data["hates"])
