from django.apps import AppConfig

from utils.tasks import create_periodic_task


class PasswordsConfig(AppConfig):
    name = "passwords"

    def ready(self) -> None:
        from .tasks import scrape_all_from_html

        create_periodic_task(scrape_all_from_html, 600, name="passwords-scraper")
