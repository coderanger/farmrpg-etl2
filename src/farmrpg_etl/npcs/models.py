import pghistory
from django.core.exceptions import ValidationError
from django.db import models

from ..items.models import Item


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class NPC(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.CharField(max_length=255)
    image_oct = models.CharField(max_length=255, null=True, blank=True)
    image_dec = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    is_available = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NPC"
        verbose_name_plural = "NPCs"

    def __str__(self) -> str:
        return self.name


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class NPCItem(models.Model):
    RELATIONSHIP_CAN_SEND = "can_send"
    RELATIONSHIP_LOVES = "loves"
    RELATIONSHIP_LIKES = "likes"
    RELATIONSHIP_HATES = "hates"
    RELATIONSHIPS = [
        (RELATIONSHIP_CAN_SEND, "Can Be Given "),
        (RELATIONSHIP_LOVES, "Loves"),
        (RELATIONSHIP_LIKES, "Likes"),
        (RELATIONSHIP_HATES, "Hates"),
    ]
    npc = models.ForeignKey(NPC, on_delete=models.CASCADE, related_name="npc_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="npc_items")
    relationship = models.CharField(max_length=32, choices=RELATIONSHIPS)
    special_xp = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NPC item"
        verbose_name_plural = "NPC items"
        constraints = [
            models.UniqueConstraint(fields=["npc", "item"], name="npc_item"),
        ]


class NPCSpecialItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(special_xp__isnull=False)


class NPCSpecialItem(NPCItem):
    objects = NPCSpecialItemManager()

    def clean(self):
        if self.special_xp is None:
            raise ValidationError("Special items must have a special XP")
        return super().clean()

    class Meta:
        verbose_name = "NPC special item"
        verbose_name_plural = "NPC special items"
        proxy = True


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class NPCReward(models.Model):
    npc = models.ForeignKey(NPC, on_delete=models.CASCADE, related_name="npc_rewards")
    level = models.IntegerField()
    order = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="npc_rewards")
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NPC reward"
        verbose_name_plural = "NPC rewards"
        constraints = [
            models.UniqueConstraint(
                fields=["npc", "level", "order"], name="npc_level_order"
            ),
        ]
