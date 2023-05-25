import pghistory
from django.db import models

from items.models import Item


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at", "completed_count"])
class Quest(models.Model):
    npc = models.CharField(max_length=255, db_index=True)
    npc_img = models.CharField(max_length=255)
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    pred = models.ForeignKey(
        "self",
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dependent_quests",
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    main_quest = models.BooleanField()
    description = models.TextField()

    required_silver = models.BigIntegerField()
    required_farming_level = models.IntegerField()
    required_fishing_level = models.IntegerField()
    required_crafting_level = models.IntegerField()
    required_exploring_level = models.IntegerField()
    required_cooking_level = models.IntegerField()
    required_tower_level = models.IntegerField()
    required_npc_id = models.IntegerField()
    required_npc_level = models.IntegerField()

    reward_silver = models.BigIntegerField()
    reward_gold = models.IntegerField()

    completed_count = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


@pghistory.track(pghistory.Snapshot())
class QuestItemRequired(models.Model):
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name="required_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="required_for_quests"
    )
    quantity = models.IntegerField()


@pghistory.track(pghistory.Snapshot())
class QuestItemReward(models.Model):
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name="reward_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="reward_for_quests"
    )
    quantity = models.IntegerField()


class Questline(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=255)
    automatic = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class QuestlineStep(models.Model):
    questline = models.ForeignKey(
        Questline, on_delete=models.CASCADE, related_name="steps"
    )
    order = models.IntegerField()
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name="questlines"
    )

    class Meta:
        ordering = ["questline", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["questline", "quest"], name="questline_quest"
            )
        ]
