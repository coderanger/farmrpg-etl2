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
    output_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="community_center_outputs"
    )
    output_quantity = models.BigIntegerField()
    progress = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.date)
