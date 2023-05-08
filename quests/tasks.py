import structlog
from asgiref.sync import sync_to_async
from toposort import toposort_flatten

from utils.http import client

from .models import Quest, QuestItemRequired, QuestItemReward
from .serializers import QuestAPISerializer

log = structlog.stdlib.get_logger(mod="quests.tasks")


async def update_items(quest_id: int, model: type, items: str):
    all_items = {}
    for chunk in items.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "|" not in chunk:
            log.error("Error in quest item chunk", quest=quest_id, chunk=chunk)
        raw_item_id, raw_quantity = chunk.split("|")
        item_id = int(raw_item_id)
        quantity = int(raw_quantity)
        await model.objects.aupdate_or_create(
            quest_id=quest_id, item_id=item_id, defaults={"quantity": quantity}
        )
        all_items[item_id] = quantity
    await model.objects.filter(quest_id=quest_id).exclude(
        item_id__in=all_items.keys()
    ).adelete()


async def scrape_all_from_api():
    log.debug("Scraping quests from API")
    resp = await client.get("/api/quests/")
    resp.raise_for_status()
    data = resp.json()

    # Do a quick toposort on pred_id. It would work without this but it might take a lot
    # of loading passes.
    by_id = {row["id"]: row for row in data}
    topo_input = {
        row["id"]: () if row["pred_id"] == 0 else {row["pred_id"]} for row in data
    }

    import_count = 0
    for quest_id in toposort_flatten(topo_input, sort=False):
        log.debug("Updating quest from API", id=quest_id)
        row = by_id[quest_id]
        try:
            required_items = row.pop("required_items")
            reward_items = row.pop("reward_items")
            quest = await Quest.objects.filter(id=row["id"]).afirst()
            ser = QuestAPISerializer(instance=quest, data=row)
            await sync_to_async(lambda: ser.is_valid(raise_exception=True))()
            await sync_to_async(ser.save)()
            await update_items(row["id"], QuestItemRequired, required_items)
            await update_items(row["id"], QuestItemReward, reward_items)
            import_count += 1
        except Exception:
            # Keep trying to rest in case this is just an eventual consistency glitch.
            log.exception("Error loading quest", id=row["id"])
    log.info("Finished scraping quests from API", count=import_count)
