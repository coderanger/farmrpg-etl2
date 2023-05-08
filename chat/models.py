import pghistory
from django.db import models

from users.models import User


class Message(models.Model):
    room = models.CharField(max_length=255, db_index=True)
    ts = models.DateTimeField()
    emblem = models.CharField(max_length=255)
    username = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
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
