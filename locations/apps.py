from django.apps import AppConfig

from utils.tasks import create_periodic_task


class LocationsConfig(AppConfig):
    name = "locations"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html, update_crop_drop_rates

        create_periodic_task(scrape_all_from_html, 3600, name="locations-scraper")
        create_periodic_task(
            update_crop_drop_rates, 43200, name="update-crop-drop-rates"
        )
