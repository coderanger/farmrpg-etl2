import pghistory
from django.db import models

from ..users.models import User


class GameChat(models.Model):
    user_id = models.IntegerField()
    chat_datetime = models.DateTimeField()
    chat_text = models.TextField(
        db_collation="utf8mb4_0900_ai_ci", blank=True, null=True
    )
    chat_room = models.CharField(max_length=150)
    chat_css = models.CharField(max_length=10)
    emblem_img = models.CharField(max_length=250)
    chat_clan_id = models.IntegerField()
    level = models.IntegerField()
    deleted = models.IntegerField()
    patreon3 = models.IntegerField()
    patreon2 = models.IntegerField()
    patreon4 = models.IntegerField()
    patreon_chat = models.IntegerField()
    flags = models.IntegerField()
    show = models.IntegerField()
    claim_item_id = models.IntegerField()
    claimed_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = "chat"


class GameEmblem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)
    created_datetime = models.DateTimeField()
    price = models.BigIntegerField()
    rarity = models.CharField(max_length=50)
    vendor_id = models.IntegerField()
    vendor_max_level = models.IntegerField()
    min_level = models.IntegerField()
    tower_level = models.IntegerField()
    img = models.CharField(max_length=250)
    category = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "emblem"


class Message(models.Model):
    room = models.CharField(max_length=255, db_index=True)
    ts = models.DateTimeField()
    emblem = models.CharField(max_length=255)
    username = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(blank=True)
    flags = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    deleted_ts = models.DateTimeField(null=True, blank=True)


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Emblem(models.Model):
    TYPE_PATREON = "patreon"
    TYPE_STAFF = "staff"
    TYPES = [
        (None, "Everyone"),
        (TYPE_PATREON, "Patreon"),
        (TYPE_STAFF, "Staff"),
    ]

    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=32, choices=TYPES, null=True)
    keywords = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at", "pk"]
