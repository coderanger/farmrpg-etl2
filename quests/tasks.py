import collections
import re

import attrs
import structlog
from asgiref.sync import sync_to_async
from toposort import toposort_flatten

from utils import roman
from utils.http import client

from .models import Quest, QuestItemRequired, QuestItemReward, Questline, QuestlineStep
from .serializers import QuestAPISerializer

log = structlog.stdlib.get_logger(mod=__name__)

QUESTLINE_NUM_RE = re.compile(
    r"^\s*(.*?)\s+(?:(?:Part (\d+))|([MCDLXVI]+))(?: - ([A-Z]))?\s*$"
)


@attrs.define
class PartialQuestline:
    quest: Quest
    weight: int


async def update_questlines():
    log.debug("Updating questlines")
    quests = Quest.objects.only("id", "title", "npc_img")
    questlines = collections.defaultdict[str, list[PartialQuestline]](list)
    async for quest in quests:
        md = QUESTLINE_NUM_RE.search(quest.title)
        if not md:
            continue
        questline_name = md.group(1)
        weight_part = md.group(2)
        weight_roman = md.group(3)
        weight = int(weight_part) if weight_part else roman.fromRoman(weight_roman)
        offset = md.group(4)
        if offset:
            weight = weight * 100 + ord(offset)
        questlines[questline_name].append(PartialQuestline(quest=quest, weight=weight))
    # Check for cases where the first quest doesn't have an I.
    async for quest in quests:
        if quest.title in questlines:
            questlines[quest.title].append(PartialQuestline(quest=quest, weight=1))
    # Update the database.
    for title, data in questlines.items():
        # First check if it exists and is not automatic, if so then we ignore
        # because we want to keep the manual override.
        if await Questline.objects.filter(title=title, automatic=False).aexists():
            continue
        data.sort(key=lambda pq: pq.weight)
        ql, _ = await Questline.objects.aupdate_or_create(
            title=title,
            defaults={
                "image": data[0].quest.npc_img,
                "automatic": True,
            },
        )
        seen_ids = []
        for i, pq in enumerate(data):
            step, _ = await QuestlineStep.objects.aupdate_or_create(
                questline=ql, quest_id=pq.quest.id, defaults={"order": i}
            )
            seen_ids.append(step.id)
        await QuestlineStep.objects.filter(questline=ql).exclude(
            id__in=seen_ids
        ).adelete()


async def update_items(quest_id: int, model: type, items: str):
    all_items = {}
    for i, chunk in enumerate(items.split(",")):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "|" not in chunk:
            log.error("Error in quest item chunk", quest=quest_id, chunk=chunk)
        raw_item_id, raw_quantity = chunk.split("|")
        item_id = int(raw_item_id)
        quantity = int(raw_quantity)
        await model.objects.aupdate_or_create(
            quest_id=quest_id,
            item_id=item_id,
            defaults={"quantity": quantity, "order": i},
        )
        all_items[item_id] = quantity
    await model.objects.filter(quest_id=quest_id).exclude(
        item_id__in=all_items.keys()
    ).adelete()


async def scrape_all_from_api():
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
    await update_questlines()
    return import_count
