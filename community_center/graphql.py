from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.CommunityCenter)
class CommunityCenterFilter:
    date: auto
    input_item: auto
    output_item: auto


@gql.django.type(models.CommunityCenter, filters=CommunityCenterFilter)
class CommunityCenter:
    id: int
    date: auto
    input_item: Item
    input_quantity: auto
    output_gold: auto
    output_item: Item | None
    output_quantity: auto
    progress: auto
