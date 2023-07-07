import strawberry
from strawberry import auto

from items.graphql import Item

from . import models
from .graphql_extra import CommunityCenterOrder


@strawberry.django.filter(models.CommunityCenter)
class CommunityCenterFilter:
    date: auto
    input_item: auto
    output_item: auto


@strawberry.django.type(
    models.CommunityCenter,
    filters=CommunityCenterFilter,
    order=CommunityCenterOrder,
    pagination=True,
)
class CommunityCenter:
    id: int
    date: auto
    input_item: Item
    input_quantity: auto
    output_gold: auto
    output_item: Item | None
    output_quantity: auto
    progress: auto
