import datetime
from typing import Iterable
from zoneinfo import ZoneInfo

from django.contrib.syndication.views import Feed

from .models import Update

SERVER_TIME = ZoneInfo("America/Chicago")


class UpdatesFeed(Feed):
    title = "Farm RPG game updates"
    link = "https://farmrpg.com/index.php#!/about.php"
    description = "Patch notes and other game updates for Farm RPG."

    def items(self) -> Iterable[Update]:
        now = datetime.datetime.now(tz=SERVER_TIME)
        today = now.date()
        is_late = now.hour >= 17  # Assuming FS is done with updates around 5PM.
        if is_late:
            today = today - datetime.timedelta(days=1)
        return Update.objects.filter(date__lte=today)[:25]

    def item_title(self, update: Update) -> str:
        return update.date.strftime("Farm RPG: %A %B %d, %Y")

    def item_description(self, update: Update) -> str:
        return update.clean_content

    def item_pubdate(self, update: Update) -> datetime.datetime:
        return datetime.datetime.combine(
            update.date,
            datetime.time(hour=17),
            tzinfo=SERVER_TIME,
        )

    def item_link(self, update: Update) -> str:
        return f"https://farmrpg.com/index.php#!/about.php?id={update.id}"
