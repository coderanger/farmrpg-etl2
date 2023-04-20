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
