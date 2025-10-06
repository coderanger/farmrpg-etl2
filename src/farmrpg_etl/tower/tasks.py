import structlog

from ..utils.http import client
from .models import TowerReward

log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_api() -> None:
    resp = await client.get("/api.php", params={"method": "tower"})
    resp.raise_for_status()
    data = resp.json()

    for level_data in data["tower_levels"]:
        log.debug("Updating tower level", level_=level_data["level"])
        order = 1
        for item_id, item_quantity in [
            (level_data["item1"], level_data["item1_amt"]),
            (level_data["item2"], level_data["item2_amt"]),
            (level_data["item3"], level_data["item3_amt"]),
        ]:
            if item_id == 0:
                continue
            await TowerReward.objects.aupdate_or_create(
                level=level_data["level"],
                order=order,
                defaults={"item_id": item_id, "item_quantity": item_quantity},
            )
            order += 1
        if level_data["gold"] != 0:
            await TowerReward.objects.aupdate_or_create(
                level=level_data["level"],
                order=order,
                defaults={"gold": level_data["gold"]},
            )
            order += 1
        if level_data["silver"] != 0:
            await TowerReward.objects.aupdate_or_create(
                level=level_data["level"],
                order=order,
                defaults={"silver": level_data["silver"]},
            )
            order += 1
