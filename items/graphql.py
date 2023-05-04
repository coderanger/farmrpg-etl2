from typing import TYPE_CHECKING, Annotated

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from . import models

if TYPE_CHECKING:
    from locations.graphql import LocationItem
    from pets.graphql import PetItem
    from quests.graphql import QuestItemRequired, QuestItemReward


@gql.django.filters.filter(models.Item)
class ItemFilter:
    id: auto
    name: auto


@gql.django.type(models.Item, filters=ItemFilter)
class Item:
    id: int
    name: auto
    image: auto
    type: auto
    xp: auto
    can_buy: auto
    can_sell: auto
    can_mail: auto
    can_craft: auto
    can_master: auto
    description: auto
    buy_price: auto
    sell_price: auto
    crafting_level: auto
    base_yield_minutes: auto
    min_mailable_level: auto
    required_for_quests: list[
        Annotated["QuestItemRequired", gql.lazy("quests.graphql")]
    ]
    reward_for_quests: list[Annotated["QuestItemReward", gql.lazy("quests.graphql")]]
    pet_items: list[Annotated["PetItem", gql.lazy("pets.graphql")]]
    location_items: list[Annotated["LocationItem", gql.lazy("locations.graphql")]]
