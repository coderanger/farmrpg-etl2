from django.apps import AppConfig

from utils.tasks import create_periodic_task


class NPCSConfig(AppConfig):
    name = "npcs"
    verbose_name = "NPCs"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html

        create_periodic_task(scrape_all_from_html, 3600, name="npcs-scraper")
