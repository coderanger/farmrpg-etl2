from django.apps import AppConfig

from ..utils.tasks import create_periodic_task


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farmrpg_etl.chat"

    def ready(self) -> None:
        from .tasks import scrape_all_chat, scrape_all_emblems, scrape_all_flags

        # TODO handle creating room docs like the old code.
        create_periodic_task(scrape_all_chat, 1, name="chat-scraper")
        create_periodic_task(scrape_all_flags, 30, name="chat-flags-scraper")

        create_periodic_task(scrape_all_emblems, 3600, name="emblems-scraper")
