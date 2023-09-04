from django.db import models


class Cron(models.Model):
    name = models.CharField(max_length=255, unique=True)
    cronspec = models.CharField(max_length=255)
    previous_started_at = models.DateTimeField(null=True, blank=True)
    previous_finished_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    previous_output = models.TextField(null=True, blank=True)
    previous_error = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
