import strawberry
from strawberry import auto

from items.graphql import ItemOrder

from . import models


@strawberry.django.filter(models.Quest)
class QuestFilter:
    id: auto
    title: auto
    clean_title: auto


@strawberry.django.order(models.Quest)
class QuestOrder:
    id: auto
    title: auto
    clean_title: auto
    created_at: auto


@strawberry.django.order(models.QuestItemRequired)
class QuestItemRequiredOrder:
    id: auto
    quest: QuestOrder
    item: ItemOrder
    quantity: auto
    order: auto


@strawberry.django.order(models.QuestItemReward)
class QuestItemRewardOrder:
    id: auto
    quest: QuestOrder
    item: ItemOrder
    quantity: auto
    order: auto


@strawberry.django.filter(models.Questline)
class QuestlineFilter:
    id: int
    title: auto


@strawberry.django.order(models.Questline)
class QuestlineOrder:
    id: auto
    title: auto
