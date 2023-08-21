from django.contrib import admin

from .models import Cron


@admin.register(Cron)
class CronAdmin(admin.ModelAdmin):
    list_display = ["name", "cronspec", "_admin_is_running", "_admin_has_error"]

    @admin.display(description="Is running", boolean=True)
    def _admin_is_running(self, obj: Cron) -> bool:
        return obj.previous_started_at is not None and (
            obj.previous_finished_at is None
            or obj.previous_finished_at < obj.previous_started_at
        )

    @admin.display(description="Has error", boolean=True)
    def _admin_has_error(self, obj: Cron) -> bool:
        return obj.previous_error is not None
