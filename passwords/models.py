import pghistory
from django.db import models

from items.models import Item


class PasswordGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Password(models.Model):
    group = models.ForeignKey(
        PasswordGroup,
        on_delete=models.CASCADE,
        related_name="passwords",
        default=0,
    )
    password = models.CharField(max_length=255, unique=True)
    clue1 = models.TextField(null=True, blank=True)
    clue2 = models.TextField(null=True, blank=True)
    clue3 = models.TextField(null=True, blank=True)

    reward_silver = models.BigIntegerField(default=0)
    reward_gold = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.password


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class PasswordItem(models.Model):
    password = models.ForeignKey(
        Password, on_delete=models.CASCADE, related_name="reward_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="password_items"
    )
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["password", "item"], name="password_item")
        ]
