import pghistory
from django.db import models

from ..items.models import Item


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


class DropRates(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="drop_rates",
        null=True,
        blank=True,
    )
    seed = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="drop_rates",
        null=True,
        blank=True,
    )
    iron_depot = models.BooleanField(null=True, blank=True)
    runecube = models.BooleanField(null=True, blank=True)
    manual_fishing = models.BooleanField(null=True, blank=True)
    hash = models.BigIntegerField(null=True, blank=True)
    compute_time = models.FloatField(null=True, blank=True)

    silver_per_hit = models.FloatField(null=True, blank=True)
    xp_per_hit = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "drop rates"
        ordering = ["location", "seed", "runecube", "pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["location", "seed", "iron_depot", "runecube", "manual_fishing"],
                name="location_flags",
            ),
            models.CheckConstraint(
                check=models.Q(location=None, seed__isnull=False)
                | models.Q(location__isnull=False, seed=None),
                name="location_or_seed",
            ),
        ]

    def __str__(self) -> str:
        parts = []
        if self.location is not None:
            parts.append(self.location.name)
        elif self.seed is not None:
            parts.append(self.seed.name)
        if self.runecube:
            parts.append("runecube")
        if self.iron_depot:
            parts.append("iron_depot")
        if self.manual_fishing:
            parts.append("manual_fishing")
        if len(parts) == 1:
            parts.append("normal")
        return " ".join(parts)


class DropRatesItem(models.Model):
    drop_rates = models.ForeignKey(
        DropRates, on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="drop_rates_items"
    )
    rate = models.FloatField()
