from django.apps import AppConfig

from ..utils.tasks import create_periodic_task


class NPCSConfig(AppConfig):
    name = "farmrpg_etl.npcs"
    verbose_name = "NPCs"

    def ready(self) -> None:
        from .tasks import scrape_all_from_api

        create_periodic_task(scrape_all_from_api, 3600, name="npcs-scraper")
