from typing import TYPE_CHECKING, Annotated, Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item, ItemFilter, ItemOrder

from . import models

if TYPE_CHECKING:
    from quests.graphql import Quest


@gql.django.filters.filter(models.NPC)
class NPCFilter:
    id: auto
    name: auto
    short_name: auto
    is_available: auto


@gql.django.ordering.order(models.NPC)
class NPCOrder:
    id: auto
    name: auto
    short_name: auto


@gql.django.type(models.NPC, filters=NPCFilter, order=NPCOrder)
class NPC:
    id: int
    name: auto
    image: auto
    short_name: auto
    is_available: auto

    npc_items: list["NPCItem"]
    npc_rewards: list["NPCReward"]

    quests: list[Annotated["Quest", gql.lazy("quests.graphql")]]


@gql.django.filters.filter(models.NPCItem)
class NPCItemFilter:
    npc: NPCFilter
    item: ItemFilter
    relationship: auto


@gql.django.ordering.order(models.NPCItem)
class NPCItemOrder:
    npc: NPCOrder
    item: ItemOrder
    relationship: auto


@gql.django.type(models.NPCItem, filters=NPCItemFilter, order=NPCItemOrder)
class NPCItem:
    npc: NPC
    item: Item
    relationship: auto


@gql.django.filters.filter(models.NPCReward)
class NPCRewardFilter:
    npc: NPCFilter
    item: ItemFilter


@gql.django.ordering.order(models.NPCReward)
class NPCRewardOrder:
    npc: NPCOrder
    item: ItemOrder
    level: auto
    order: auto


@gql.django.type(models.NPCReward, filters=NPCRewardFilter, order=NPCRewardOrder)
class NPCReward:
    npc: NPC
    level: auto
    order: auto
    item: Item
    quantity: auto
