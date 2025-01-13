import pghistory
from django.db import models

from ..items.models import Item

@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Pet(models.Model):
    game_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=255)
    cost = models.BigIntegerField()
    order = models.IntegerField()

    required_farming_level = models.IntegerField(default=0)
    required_fishing_level = models.IntegerField(default=0)
    required_crafting_level = models.IntegerField(default=0)
    required_exploring_level = models.IntegerField(default=0)
    required_cooking_level = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@pghistory.track(pghistory.Snapshot())
class PetItem(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="pet_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="pet_items")
    level = models.IntegerField()
    order = models.IntegerField()
