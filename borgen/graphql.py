import strawberry
from strawberry import auto

from items.graphql import Item

from . import models


@strawberry.django.filter(models.BorgenItem)
class BorgenItemFilter:
    date: auto
    item: auto


@strawberry.django.type(models.BorgenItem, filters=BorgenItemFilter)
class BorgenItem:
    id: int
    date: auto
    item: Item
    price: auto
