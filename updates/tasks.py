import structlog

from utils.http import client

from .models import Update
from .parsers import parse_updates

log = structlog.stdlib.get_logger(mod="updates.tasks")


async def scrape_all_from_html():
    log.debug("Scraping updates from HTML")
    resp = await client.get("/about.php")
    resp.raise_for_status()

    for data in parse_updates(resp.content):
        await Update.objects.aupdate_or_create(
            date=data["date"],
            defaults={
                "content": data["content"],
                "clean_content": data["clean_content"],
                "text_content": data["text_content"],
            },
        )
    log.debug("Finished scraping updated from HTML")
