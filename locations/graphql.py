from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.Location)
class LocationFilter:
    id: auto
    type: auto
    name: auto


@gql.django.type(models.Location, filters=LocationFilter)
class Location:
    id: int = gql.field(resolver=lambda self: self.game_id)
    type: auto
    name: auto
    image: auto
    base_drop_rate: auto

    location_items: list["LocationItem"]


@gql.django.type(models.LocationItem)
class LocationItem:
    location: Location
    item: Item
    sometimes: auto
