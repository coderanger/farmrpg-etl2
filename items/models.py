import pghistory
from django.db import models


@pghistory.track(pghistory.Snapshot())
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
