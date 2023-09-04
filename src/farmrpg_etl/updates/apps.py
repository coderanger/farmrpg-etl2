from django.apps import AppConfig

from ..utils.tasks import create_periodic_task


class UpdatesConfig(AppConfig):
    name = "farmrpg_etl.updates"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html

        create_periodic_task(scrape_all_from_html, 600, name="updates-scraper")
