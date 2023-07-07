from typing import TYPE_CHECKING, Annotated

import strawberry
from strawberry import auto

from items.graphql import Item, ItemFilter, ItemOrder
from quests.graphql_extra import QuestFilter, QuestOrder

from . import models

if TYPE_CHECKING:
    from quests.graphql import Quest


@strawberry.django.filter(models.NPC)
class NPCFilter:
    id: auto
    name: auto
    short_name: auto
    is_available: auto


@strawberry.django.order(models.NPC)
class NPCOrder:
    id: auto
    name: auto
    short_name: auto


@strawberry.django.type(models.NPC, filters=NPCFilter, order=NPCOrder)
class NPC:
    id: int
    name: auto
    image: auto
    short_name: auto
    is_available: auto

    npc_items: list["NPCItem"]
    npc_rewards: list["NPCReward"]

    quests: list[
        Annotated["Quest", strawberry.lazy("quests.graphql")]
    ] = strawberry.django.field(filters=QuestFilter, order=QuestOrder)


@strawberry.django.filter(models.NPCItem)
class NPCItemFilter:
    npc: NPCFilter
    item: ItemFilter
    relationship: auto


@strawberry.django.order(models.NPCItem)
class NPCItemOrder:
    npc: NPCOrder
    item: ItemOrder
    relationship: auto


@strawberry.django.type(models.NPCItem, filters=NPCItemFilter, order=NPCItemOrder)
class NPCItem:
    npc: NPC
    item: Item
    relationship: auto


@strawberry.django.filter(models.NPCReward)
class NPCRewardFilter:
    npc: NPCFilter
    item: ItemFilter


@strawberry.django.order(models.NPCReward)
class NPCRewardOrder:
    npc: NPCOrder
    item: ItemOrder
    level: auto
    order: auto


@strawberry.django.type(models.NPCReward, filters=NPCRewardFilter, order=NPCRewardOrder)
class NPCReward:
    npc: NPC
    level: auto
    order: auto
    item: Item
    quantity: auto
