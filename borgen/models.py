import pghistory
from django.db import models

from items.models import Item


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class BorgenItem(models.Model):
    date = models.DateField()
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="borgen_items"
    )
    price = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "item"]
        constraints = [
            models.UniqueConstraint(fields=["date", "item"], name="date_item")
        ]

    def __str__(self) -> str:
        return f"{self.date} {self.item.name}"
