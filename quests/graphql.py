from typing import Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item, ItemOrder

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


@gql.django.type(models.Quest, filters=QuestFilter, order=QuestOrder, pagination=True)
class Quest:
    id: int
    npc: auto
    npc_img: auto
    title: auto
    author: auto
    pred: Optional["Quest"]
    dependent_quests: list["Quest"]
    start_date: auto
    end_date: auto
    main_quest: auto
    description: auto
    clean_description: auto

    required_silver: float
    required_farming_level: auto
    required_fishing_level: auto
    required_crafting_level: auto
    required_exploring_level: auto
    required_cooking_level: auto
    required_tower_level: auto
    required_npc_id: auto
    required_npc_level: auto
    required_items: list["QuestItemRequired"]

    reward_silver: float
    reward_gold: auto
    reward_items: list["QuestItemReward"]

    questlines: list["QuestlineStep"]

    completed_count: auto
    is_hidden: bool


@gql.django.ordering.order(models.QuestItemRequired)
class QuestItemRequiredOrder:
    id: auto
    quest: QuestOrder
    item: ItemOrder
    quantity: auto
    order: auto


@gql.django.type(models.QuestItemRequired, order=QuestItemRequiredOrder)
class QuestItemRequired:
    id: int
    quest: Quest
    item: Item
    quantity: int
    order: auto


@gql.django.ordering.order(models.QuestItemReward)
class QuestItemRewardOrder:
    id: auto
    quest: QuestOrder
    item: ItemOrder
    quantity: auto
    order: auto


@gql.django.type(models.QuestItemReward, order=QuestItemRewardOrder)
class QuestItemReward:
    id: int
    quest: Quest
    item: Item
    quantity: int
    order: auto


@gql.django.filters.filter(models.Questline)
class QuestlineFilter:
    id: int
    title: auto


@gql.django.ordering.order(models.Questline)
class QuestlineOrder:
    id: auto
    title: auto


@gql.django.type(models.Questline, filters=QuestlineFilter, order=QuestlineOrder)
class Questline:
    id: int
    title: auto
    image: auto
    automatic: auto
    steps: list["QuestlineStep"]


@gql.django.type(models.QuestlineStep)
class QuestlineStep:
    questline: Questline
    order: auto
    quest: Quest
