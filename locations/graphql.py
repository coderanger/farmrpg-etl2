from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.Location)
class LocationFilter:
    id: auto
    type: auto
    name: auto


@gql.django.ordering.order(models.Location)
class LocationOrder:
    # It's annoying to have to call it game_id but there's no provisions for
    # custom ordering so I can't make a lie-alias like in the main type. Oh well.
    id: auto
    game_id: auto
    type: auto
    name: auto


@gql.django.type(models.Location, filters=LocationFilter, order=LocationOrder)
class Location:
    id: int = gql.field(resolver=lambda self: self.game_id)
    type: auto
    name: auto
    image: auto
    base_drop_rate: auto

    location_items: list["LocationItem"]
    drop_rates: list["DropRates"]


@gql.django.type(models.LocationItem)
class LocationItem:
    location: Location
    item: Item
    sometimes: auto


@gql.django.type(models.DropRates)
class DropRates:
    location: Location | None
    seed: Item | None
    iron_depot: auto
    manual_fishing: auto
    runecube: auto
    silver_per_hit: auto
    xp_per_hit: auto

    items: list["DropRatesItem"]


@gql.django.type(models.DropRatesItem)
class DropRatesItem:
    drop_rates: DropRates
    item: Item
    rate: auto
