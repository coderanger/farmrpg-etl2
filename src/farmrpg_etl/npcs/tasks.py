import structlog

from ..utils.http import client
from .models import NPC, NPCItem, NPCReward

log = structlog.stdlib.get_logger(mod=__name__)

NPC_ALIASES = {
    "charles": "charles horsington iii",
    "cpt thomas": "captain thomas",
}


async def _update_items(npc: NPC, relationship: str, item_ids: str) -> None:
    seen_item_ids = []
    for item_id in item_ids.split(","):
        if item_id.strip() == "":
            continue
        await NPCItem.objects.aupdate_or_create(
            npc=npc,
            item_id=int(item_id.strip()),
            defaults={"relationship": relationship},
        )
        seen_item_ids.append(item_id)
    await NPCItem.objects.filter(npc=npc, relationship=relationship).exclude(
        item_id__in=seen_item_ids
    ).adelete()


async def _update_reward(
    npc: NPC, level: int, order: int, item_id: int, quantity: int
) -> None:
    if item_id == 0 or quantity == 0:
        # Delete it.
        await NPCReward.objects.filter(npc=npc, level=level, order=order).adelete()
    else:
        # Upsert.
        await NPCReward.objects.aupdate_or_create(
            npc=npc,
            level=level,
            order=order,
            defaults={
                "item_id": item_id,
                "quantity": quantity,
            },
        )


async def scrape_all_from_api() -> None:
    resp = await client.get("/api.php", params={"method": "npcs"})
    resp.raise_for_status()
    data = resp.json()

    npcs_by_name: dict[str, NPC] = {}
    for npc_data in data["npcs"]:
        log.debug("Updating NPC", id=npc_data.get("user_id"), name=npc_data.get("name"))
        npc, _ = await NPC.objects.aupdate_or_create(
            id=npc_data["user_id"],
            defaults={
                "name": npc_data["name"],
                "image": npc_data["img"],
                "image_oct": npc_data.get("img_oct"),
                "image_dec": npc_data.get("img_dec"),
                "is_available": npc_data.get("friendship") == 1,
            },
        )
        npcs_by_name[npc.name.lower()] = npc
        await _update_items(npc, "can_send", npc_data["can_be_given_items"])
        await _update_items(npc, "loves", npc_data["love_items"])
        await _update_items(npc, "likes", npc_data["like_items"])
        await _update_items(npc, "hates", npc_data["hate_items"])

    for reward_data in data["npc_rewards"]:
        log.debug(
            "Updating NPC reward",
            id=reward_data.get("id"),
            npc=reward_data.get("npc"),
            level_=reward_data.get("level"),
        )
        npc_name = reward_data["npc"].lower()
        npc_name = NPC_ALIASES.get(npc_name, npc_name)
        npc = npcs_by_name[npc_name]
        await _update_reward(
            npc, reward_data["level"], 0, reward_data["item1"], reward_data["item1_amt"]
        )
        await _update_reward(
            npc, reward_data["level"], 1, reward_data["item2"], reward_data["item2_amt"]
        )
        await _update_reward(
            npc, reward_data["level"], 2, reward_data["item3"], reward_data["item3_amt"]
        )
