import structlog

from utils.http import client

from .models import Password, PasswordItem
from .parsers import parse_password_log

log = structlog.stdlib.get_logger(mod="passwords.tasks")


async def scrape_all_from_html():
    log.debug("Scraping passwords from HTML")
    resp = await client.get("/TODO")
    resp.raise_for_status()

    for data in parse_password_log(resp.content):
        password, _ = await Password.objects.aupdate_or_create(
            password=data["password"],
            defaults={
                "reward_silver": data["reward_silver"],
                "reward_gold": data["reward_gold"],
            },
        )

        for item in data["reward_items"]:
            await PasswordItem.objects.aupdate_or_create(
                password=password,
                item_id=item["item"],
                defaults={"quantity": item["quantity"]},
            )
        await PasswordItem.objects.filter(password=password).exclude(
            item_id__in=[item["item"] for item in data["reward_items"]]
        ).adelete()
    log.debug("Finished scraping passwords from HTML")
