from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item, ItemOrder

from . import models


@gql.django.ordering.order(models.Trade)
class TradeOrder:
    first_seen: auto
    last_seen: auto
    input_item: ItemOrder
    output_item: ItemOrder


@gql.django.type(models.Trade, order=TradeOrder)
class Trade:
    id: int
    input_item: Item
    input_quantity: auto
    output_item: Item
    output_quantity: auto
    oneshot: auto
    first_seen: auto
    last_seen: auto
