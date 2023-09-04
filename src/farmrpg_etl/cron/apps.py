from django.apps import AppConfig


class CronConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farmrpg_etl.cron"

    def ready(self) -> None:
        from .tasks import start_cron

        start_cron()
