import pghistory
from django.db import models


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Item(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    xp = models.IntegerField()
    can_buy = models.BooleanField()
    can_sell = models.BooleanField()
    can_mail = models.BooleanField()
    can_craft = models.BooleanField()
    can_master = models.BooleanField()
    description = models.TextField(blank=True)
    buy_price = models.IntegerField()
    sell_price = models.IntegerField()
    crafting_level = models.IntegerField()
    base_yield_minutes = models.IntegerField()
    min_mailable_level = models.IntegerField()
    reg_weight = models.IntegerField()
    runecube_weight = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
