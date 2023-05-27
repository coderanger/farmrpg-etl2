import pghistory
from django.db import models

from items.models import Item


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class CommunityCenter(models.Model):
    date = models.DateField(unique=True)
    input_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="community_center_inputs"
    )
    input_quantity = models.BigIntegerField()
    output_gold = models.IntegerField(null=True, blank=True)
    output_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="community_center_outputs",
        null=True,
        blank=True,
    )
    output_quantity = models.IntegerField(null=True, blank=True)
    progress = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.date)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    output_gold__isnull=False,
                    output_item=None,
                    output_quantity=None,
                )
                | models.Q(
                    output_gold=None,
                    output_item__isnull=False,
                    output_quantity__isnull=False,
                ),
                name="communitycenter_only_one_output",
            )
        ]
