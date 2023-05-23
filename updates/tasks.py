import structlog

from utils.http import client

from .models import Update
from .parsers import parse_updates

log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_html():
    resp = await client.get("/about.php?all=1")
    resp.raise_for_status()

    for parsed in parse_updates(resp.content):
        await Update.objects.aupdate_or_create(
            id=parsed.id,
            defaults={
                "date": parsed.date,
                "content": parsed.content,
                "clean_content": parsed.clean_content,
                "text_content": parsed.text_content,
            },
        )
