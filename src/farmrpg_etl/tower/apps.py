from django.apps import AppConfig

from ..utils.tasks import create_periodic_task


class TowerConfig(AppConfig):
    name = "farmrpg_etl.tower"

    def ready(self) -> None:
        from .tasks import scrape_all_from_api

        create_periodic_task(scrape_all_from_api, 3600, name="tower-scraper")
