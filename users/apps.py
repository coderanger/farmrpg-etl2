from django.apps import AppConfig

from utils.tasks import create_periodic_task


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        from .tasks import scrape_all_from_online, scrape_all_from_stafflist

        create_periodic_task(scrape_all_from_online, 600, name="users-online-scraper")
        create_periodic_task(
            scrape_all_from_stafflist, 3600, name="users-staff-scraper"
        )
