import strawberry
from strawberry import auto

from items.graphql import Item

from . import models


@strawberry.django.filter(models.ProfileBackground)
class ProfileBackgroundFilter:
    id: auto
    game_id: auto
    name: auto


@strawberry.django.order(models.ProfileBackground)
class ProfileBackgroundOrder:
    id: auto
    game_id: auto
    name: auto


@strawberry.django.type(
    models.ProfileBackground,
    filters=ProfileBackgroundFilter,
    order=ProfileBackgroundOrder,
)
class ProfileBackground:
    id: auto
    game_id: auto
    name: auto
    light_image: auto
    dark_image: auto
    cost_silver: float | None
    cost_gold: auto
    cost_item: Item | None
    cost_item_quantity: auto
