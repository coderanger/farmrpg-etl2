import strawberry
from strawberry import auto

from items.graphql import Item

from . import models
from .graphql_extra import TowerRewardOrder


@strawberry.django.filter(models.TowerReward)
class TowerRewardFilter:
    level: auto
    order: auto


@strawberry.django.type(
    models.TowerReward, filters=TowerRewardFilter, order=TowerRewardOrder
)
class TowerReward:
    level: auto
    order: auto
    silver: auto
    gold: auto
    item: Item | None
    item_quantity: auto
