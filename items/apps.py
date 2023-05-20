from django.apps import AppConfig

from utils.tasks import create_periodic_task


class ItemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "items"

    def ready(self) -> None:
        from .tasks import scrape_all_from_api, scrape_wishing_well_from_sheets

        create_periodic_task(scrape_all_from_api, 600, name="items-scraper")
        create_periodic_task(
            scrape_wishing_well_from_sheets, 3600, name="wishing-well-scraper"
        )
