from typing import TYPE_CHECKING, Annotated, Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from . import models

if TYPE_CHECKING:
    from locations.graphql import DropRates, DropRatesItem, LocationItem
    from npcs.graphql import NPCItem, NPCReward
    from passwords.graphql import PasswordItem
    from pets.graphql import PetItem
    from quests.graphql import QuestItemRequired, QuestItemReward
    from quizzes.graphql import QuizReward
    from exchange_center.graphql import Trade


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
    cooking_level: auto
    base_yield_minutes: auto
    min_mailable_level: auto
    locksmith_grab_bag: bool
    locksmith_gold: auto
    required_for_quests: list[
        Annotated["QuestItemRequired", gql.lazy("quests.graphql")]
    ]
    reward_for_quests: list[Annotated["QuestItemReward", gql.lazy("quests.graphql")]]
    pet_items: list[Annotated["PetItem", gql.lazy("pets.graphql")]]
    location_items: list[Annotated["LocationItem", gql.lazy("locations.graphql")]]
    drop_rates: list[Annotated["DropRates", gql.lazy("locations.graphql")]]
    drop_rates_items: list[Annotated["DropRatesItem", gql.lazy("locations.graphql")]]
    quiz_rewards: list[Annotated["QuizReward", gql.lazy("quizzes.graphql")]]
    npc_items: list[Annotated["NPCItem", gql.lazy("npcs.graphql")]]
    npc_rewards: list[Annotated["NPCReward", gql.lazy("npcs.graphql")]]
    password_items: list[Annotated["PasswordItem", gql.lazy("passwords.graphql")]]
    wishing_well_input_items: list["WishingWellItem"]
    wishing_well_output_items: list["WishingWellItem"]
    recipe_items: list["RecipeItem"]
    recipe_ingredient_tiems: list["RecipeItem"]
    locksmith_items: list["LocksmithItem"]
    locksmith_output_items: list["LocksmithItem"]
    locksmith_key: Optional["Item"]
    locksmith_key_items: list["Item"]
    cooking_recipe_item: Optional["Item"]
    cooking_recipe_cookable: Optional["Item"]
    manual_productions: list["ManualProduction"]
    exchange_center_inputs: list[
        Annotated["Trade", gql.lazy("exchange_center.graphql")]
    ]
    exchange_center_outputs: list[
        Annotated["Trade", gql.lazy("exchange_center.graphql")]
    ]


@gql.django.type(models.RecipeItem)
class RecipeItem:
    item: Item
    ingredient_item: Item
    quantity: auto


@gql.django.type(models.LocksmithItem)
class LocksmithItem:
    item: Item
    output_item: Item
    quantity_min: auto
    quantity_max: auto


@gql.django.type(models.WishingWellItem)
class WishingWellItem:
    input_item: Item
    chance: auto
    output_item: Item


@gql.django.type(models.ManualProduction)
class ManualProduction:
    item: Item
    line_one: auto
    line_two: auto
    image: auto
    value: auto
    sort: auto
