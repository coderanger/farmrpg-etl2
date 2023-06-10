from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.ProfileBackground)
class ProfileBackgroundFilter:
    id: auto
    game_id: auto
    name: auto


@gql.django.ordering.order(models.ProfileBackground)
class ProfileBackgroundOrder:
    id: auto
    game_id: auto
    name: auto


@gql.django.type(
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
