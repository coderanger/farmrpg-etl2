import strawberry
from strawberry import auto

from . import models


@strawberry.django.filter(models.Item)
class ItemFilter:
    id: auto
    name: auto
    can_mail: auto


@strawberry.django.order(models.Item)
class ItemOrder:
    id: auto
    name: auto
    created_at: auto
