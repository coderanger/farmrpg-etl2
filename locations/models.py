import pghistory
from django.db import models

from items.models import Item


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Location(models.Model):
    TYPE_EXPLORE = "explore"
    TYPE_FISHING = "fishing"
    TYPES = (
        (TYPE_EXPLORE, "Exploring"),
        (TYPE_FISHING, "Fishing"),
    )

    game_id = models.IntegerField(db_index=True)
    type = models.CharField(max_length=32, choices=TYPES, db_index=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    base_drop_rate = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game_id", "type"], name="game_id_type")
        ]

    def __str__(self) -> str:
        return self.name


@pghistory.track(pghistory.Snapshot())
class LocationItem(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="location_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="location_items"
    )
    sometimes = models.BooleanField(default=False)
