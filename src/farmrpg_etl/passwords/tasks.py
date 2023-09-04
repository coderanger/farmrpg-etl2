import structlog

from ..items.models import Item
from ..utils.http import client

from .models import Password, PasswordItem
from .parsers import parse_password_log

log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_html():
    resp = await client.get("/popwlog.php")
    resp.raise_for_status()

    for parsed in parse_password_log(resp.content):
        silver = parsed.rewards.pop("Silver", 0)
        gold = parsed.rewards.pop("Gold", 0)
        password, _ = await Password.objects.aupdate_or_create(
            password=parsed.password,
            defaults={"reward_silver": silver, "reward_gold": gold},
        )

        seen_ids = []
        for item_name, quantity in parsed.rewards.items():
            item_id = await Item.objects.values_list("id", flat=True).aget(
                name=item_name
            )
            password_item, _ = await PasswordItem.objects.aupdate_or_create(
                password=password,
                item_id=item_id,
                defaults={"quantity": quantity},
            )
            seen_ids.append(password_item.id)
        await PasswordItem.objects.filter(password=password).exclude(
            id__in=seen_ids
        ).adelete()
