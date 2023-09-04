import pghistory
from django.db import models

from ..items.models import Item


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class ProfileBackground(models.Model):
    game_id = models.IntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, unique=True)
    light_image = models.CharField(max_length=255)
    dark_image = models.CharField(max_length=255)

    cost_silver = models.BigIntegerField(null=True, blank=True)
    cost_gold = models.IntegerField(null=True, blank=True)
    cost_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="profile_background_cost_items",
        null=True,
        blank=True,
    )
    cost_item_quantity = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
