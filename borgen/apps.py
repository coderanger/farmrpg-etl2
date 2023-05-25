from django.apps import AppConfig

from utils.tasks import create_periodic_task


class BorgenConfig(AppConfig):
    name = "borgen"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html

        create_periodic_task(scrape_all_from_html, 600, name="borgens-scraper")
