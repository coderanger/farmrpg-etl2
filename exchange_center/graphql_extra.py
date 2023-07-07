import strawberry
from strawberry import auto

from items.graphql_extra import ItemOrder

from . import models


@strawberry.django.order(models.Trade)
class TradeOrder:
    first_seen: auto
    last_seen: auto
    input_item: ItemOrder
    output_item: ItemOrder


@strawberry.django.filter(models.CardsTrade)
class CardsTradeFilter:
    id: int
    is_disabled: auto


@strawberry.django.order(models.CardsTrade)
class CardsTradeOrder:
    id: auto
