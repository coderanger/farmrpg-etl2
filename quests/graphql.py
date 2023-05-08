from typing import Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.Quest)
class QuestFilter:
    id: auto


@gql.django.type(models.Quest, filters=QuestFilter)
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

    required_silver: auto
    required_farming_level: auto
    required_fishing_level: auto
    required_crafting_level: auto
    required_exploring_level: auto
    required_cooking_level: auto
    required_tower_level: auto
    required_npc_id: auto
    required_npc_level: auto
    required_items: list["QuestItemRequired"]

    reward_silver: auto
    reward_gold: auto
    reward_items: list["QuestItemReward"]

    completed_count: auto


@gql.django.type(models.QuestItemRequired)
class QuestItemRequired:
    id: int
    quest: Quest
    item: Item
    quantity: int


@gql.django.type(models.QuestItemReward)
class QuestItemReward:
    id: int
    quest: Quest
    item: Item
    quantity: int
