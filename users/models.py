import pghistory
from django.db import models


@pghistory.track(pghistory.Snapshot())
class User(models.Model):
    username = models.CharField(max_length=255, db_index=True)
    role = models.CharField(max_length=64, null=True, blank=True)
    firebase_uid = models.CharField(
        max_length=255, null=True, blank=True, db_index=True, unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
