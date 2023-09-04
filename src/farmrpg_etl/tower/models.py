from django.db import models

from ..items.models import Item


class TowerReward(models.Model):
    level = models.IntegerField()
    order = models.IntegerField()

    silver = models.BigIntegerField(null=True, blank=True)
    gold = models.IntegerField(null=True, blank=True)
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="tower_rewards",
        null=True,
        blank=True,
    )
    item_quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-level", "order"]
        constraints = [
            models.UniqueConstraint(fields=["level", "order"], name="level_order"),
            models.CheckConstraint(
                check=models.Q(
                    silver__isnull=False, gold=None, item=None, item_quantity=None
                )
                | models.Q(
                    silver=None, gold__isnull=False, item=None, item_quantity=None
                )
                | models.Q(
                    silver=None,
                    gold=None,
                    item__isnull=False,
                    item_quantity__isnull=False,
                ),
                name="only_one_type",
            ),
        ]
