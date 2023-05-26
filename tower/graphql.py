from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.TowerReward)
class TowerRewardFilter:
    level: auto
    order: auto


@gql.django.type(models.TowerReward, filters=TowerRewardFilter)
class TowerReward:
    level: auto
    order: auto
    silver: auto
    gold: auto
    item: Item | None
    item_quantity: auto
