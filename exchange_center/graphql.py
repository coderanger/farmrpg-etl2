from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.type(models.Trade)
class Trade:
    input_item: Item
    input_quantity: auto
    output_item: Item
    output_quantity: auto
    oneshot: auto
    first_seen: auto
    last_seen: auto
