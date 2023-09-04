from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from ..items.graphql import Item

from . import models


@gql.django.filters.filter(models.BorgenItem)
class BorgenItemFilter:
    date: auto
    item: auto


@gql.django.type(models.BorgenItem, filters=BorgenItemFilter)
class BorgenItem:
    id: int
    date: auto
    item: Item
    price: auto
