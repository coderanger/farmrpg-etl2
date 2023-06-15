from django.db import models
import pghistory

from items.models import Item


class Trade(models.Model):
    input_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="exchange_center_inputs"
    )
    input_quantity = models.IntegerField()
    output_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="exchange_center_outputs"
    )
    output_quantity = models.IntegerField()
    oneshot = models.BooleanField()

    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "input_item",
                    "input_quantity",
                    "output_item",
                    "output_quantity",
                    "oneshot",
                ],
                name="items",
            )
        ]

    def __str__(self) -> str:
        return f"{self.input_item.name} x{self.input_quantity} for {self.output_item.name} x{self.output_quantity}"


class TradeHistory(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="history")
    seen_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["trade", "seen_at"], name="trade_seen_at")
        ]


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class CardsTrade(models.Model):
    spades_quantity = models.IntegerField(null=True, blank=True)
    hearts_quantity = models.IntegerField(null=True, blank=True)
    diamonds_quantity = models.IntegerField(null=True, blank=True)
    clubs_quantity = models.IntegerField(null=True, blank=True)
    joker_quantity = models.IntegerField(null=True, blank=True)

    output_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="cards_trades"
    )
    output_quantity = models.IntegerField()

    is_disabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
