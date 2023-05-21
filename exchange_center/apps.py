from django.apps import AppConfig

from utils.tasks import create_periodic_task


class ExchangeCenterConfig(AppConfig):
    name = "exchange_center"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html

        create_periodic_task(scrape_all_from_html, 3600, name="exchange-center-scraper")
