from django.apps import AppConfig

from utils.tasks import create_periodic_task


class QuestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quests"

    def ready(self) -> None:
        from .tasks import scrape_all_from_api

        create_periodic_task(scrape_all_from_api, 600, name="quest-scraper")
