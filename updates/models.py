import pghistory
from django.db import models


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Update(models.Model):
    date = models.DateField(db_index=True)
    content = models.TextField()
    clean_content = models.TextField()
    text_content = models.TextField()

    annouced_discord = models.BooleanField(default=False)
    announced_reddit = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.date)
