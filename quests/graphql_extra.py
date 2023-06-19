from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import ItemOrder

from . import models


@gql.django.filters.filter(models.Quest)
class QuestFilter:
    id: auto
    title: auto


@gql.django.ordering.order(models.Quest)
class QuestOrder:
    id: auto
    title: auto
    created_at: auto


@gql.django.ordering.order(models.QuestItemRequired)
class QuestItemRequiredOrder:
    id: auto
    quest: QuestOrder
    item: ItemOrder
    quantity: auto
    order: auto


@gql.django.ordering.order(models.QuestItemReward)
class QuestItemRewardOrder:
    id: auto
    quest: QuestOrder
    item: ItemOrder
    quantity: auto
    order: auto


@gql.django.filters.filter(models.Questline)
class QuestlineFilter:
    id: int
    title: auto


@gql.django.ordering.order(models.Questline)
class QuestlineOrder:
    id: auto
    title: auto
