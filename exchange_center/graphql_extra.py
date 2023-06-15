from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql_extra import ItemOrder

from . import models


@gql.django.ordering.order(models.Trade)
class TradeOrder:
    first_seen: auto
    last_seen: auto
    input_item: ItemOrder
    output_item: ItemOrder


@gql.django.filters.filter(models.CardsTrade)
class CardsTradeFilter:
    id: int
    is_disabled: auto


@gql.django.ordering.order(models.CardsTrade)
class CardsTradeOrder:
    id: auto
