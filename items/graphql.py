from typing import TYPE_CHECKING, Annotated, Optional

from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from community_center.graphql_extra import CommunityCenterOrder
from exchange_center.graphql_extra import CardsTradeFilter, CardsTradeOrder
from pets.graphql_extra import PetItemOrder
from tower.graphql_extra import TowerRewardOrder

from . import models
from .graphql_extra import ItemFilter, ItemOrder

if TYPE_CHECKING:
    from locations.graphql import DropRates, DropRatesItem, LocationItem
    from npcs.graphql import NPCItem, NPCReward
    from passwords.graphql import PasswordItem
    from pets.graphql import PetItem
    from quests.graphql import QuestItemRequired, QuestItemReward
    from quizzes.graphql import QuizReward
    from exchange_center.graphql import Trade, CardsTrade
    from borgen.graphql import BorgenItem
    from community_center.graphql import CommunityCenter
    from pbgs.graphql import ProfileBackground
    from tower.graphql import TowerReward


@gql.django.type(models.Item, filters=ItemFilter, order=ItemOrder, pagination=True)
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
    can_cook: auto
    can_master: auto
    description: auto
    buy_price: auto
    flea_market_price: auto
    sell_price: auto
    crafting_level: auto
    cooking_level: auto
    base_yield_minutes: auto
    min_mailable_level: auto
    locksmith_grab_bag: bool
    locksmith_gold: auto
    manual_fishing_only: auto
    from_event: auto
    required_for_quests: list[
        Annotated["QuestItemRequired", gql.lazy("quests.graphql")]
    ]
    reward_for_quests: list[Annotated["QuestItemReward", gql.lazy("quests.graphql")]]
    pet_items: list[Annotated["PetItem", gql.lazy("pets.graphql")]] = gql.django.field(
        order=PetItemOrder
    )
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
    recipe_ingredient_items: list["RecipeItem"]
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
    cards_trades: list[
        Annotated["CardsTrade", gql.lazy("exchange_center.graphql")]
    ] = gql.django.field(filters=CardsTradeFilter, order=CardsTradeOrder)
    borgen_items: list[Annotated["BorgenItem", gql.lazy("borgen.graphql")]]
    community_center_inputs: list[
        Annotated["CommunityCenter", gql.lazy("community_center.graphql")]
    ] = gql.django.field(order=CommunityCenterOrder, pagination=True)
    community_center_outputs: list[
        Annotated["CommunityCenter", gql.lazy("community_center.graphql")]
    ] = gql.django.field(order=CommunityCenterOrder, pagination=True)
    profile_background_cost_items: list[
        Annotated["ProfileBackground", gql.lazy("pbgs.graphql")]
    ]
    tower_rewards: list[
        Annotated["TowerReward", gql.lazy("tower.graphql")]
    ] = gql.django.field(order=TowerRewardOrder)
    skill_level_rewards: list["SkillLevelReward"]


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
    href: auto
    value: auto
    sort: auto


@gql.django.filters.filter(models.SkillLevelReward)
class SkillLevelRewardFilter:
    id: int
    skill: auto
    level: auto


@gql.django.ordering.order(models.SkillLevelReward)
class SkillLevelRewardOrder:
    id: auto
    skill: auto
    level: auto
    order: auto


@gql.django.type(
    models.SkillLevelReward, filters=SkillLevelRewardFilter, order=SkillLevelRewardOrder
)
class SkillLevelReward:
    id: int
    skill: auto
    level: auto
    order: auto
    silver: auto
    gold: auto
    ak: auto
    item: Item | None
    item_quantity: auto
