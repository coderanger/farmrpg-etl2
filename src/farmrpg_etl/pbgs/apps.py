from django.apps import AppConfig

from ..utils.tasks import create_periodic_task


class PbgsConfig(AppConfig):
    name = "farmrpg_etl.pbgs"
    verbose_name = "Profile Backgrounds"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html

        create_periodic_task(scrape_all_from_html, 600, name="pbgs-scraper")
