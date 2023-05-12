from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.NPC)
class NPCFilter:
    id: auto
    name: auto
    short_name: auto


@gql.django.type(models.NPC, filters=NPCFilter)
class NPC:
    id: int
    name: auto
    image: auto
    short_name: auto

    npc_items: list["NPCItem"]
    npc_rewards: list["NPCReward"]


@gql.django.type(models.NPCItem)
class NPCItem:
    npc: NPC
    item: Item
    relationship: auto


@gql.django.type(models.NPCReward)
class NPCReward:
    npc: NPC
    level: auto
    order: auto
    item: Item
    quantity: auto
