import strawberry
from strawberry import auto

from items.graphql import Item

from . import models
from .graphql_extra import CardsTradeFilter, CardsTradeOrder, TradeOrder


@strawberry.django.type(models.Trade, order=TradeOrder)
class Trade:
    id: int
    input_item: Item
    input_quantity: auto
    output_item: Item
    output_quantity: auto
    oneshot: auto
    first_seen: auto
    last_seen: auto


@strawberry.django.type(
    models.CardsTrade, filters=CardsTradeFilter, order=CardsTradeOrder
)
class CardsTrade:
    id: int
    spades_quantity: auto
    hearts_quantity: auto
    diamonds_quantity: auto
    clubs_quantity: auto
    joker_quantity: auto
    output_item: Item
    output_quantity: auto
    is_disabled: auto
