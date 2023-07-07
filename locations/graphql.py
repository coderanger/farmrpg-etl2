import strawberry
from strawberry import auto

from items.graphql import Item

from . import models


@strawberry.django.filter(models.Location)
class LocationFilter:
    id: auto
    type: auto
    name: auto


@strawberry.django.order(models.Location)
class LocationOrder:
    # It's annoying to have to call it game_id but there's no provisions for
    # custom ordering so I can't make a lie-alias like in the main type. Oh well.
    id: auto
    game_id: auto
    type: auto
    name: auto


@strawberry.django.type(models.Location, filters=LocationFilter, order=LocationOrder)
class Location:
    id: int = strawberry.field(resolver=lambda self: self.game_id)
    game_id: auto
    type: auto
    name: auto
    image: auto
    base_drop_rate: auto

    location_items: list["LocationItem"]
    drop_rates: list["DropRates"]


@strawberry.django.type(models.LocationItem)
class LocationItem:
    location: Location
    item: Item
    sometimes: auto


@strawberry.django.type(models.DropRates)
class DropRates:
    location: Location | None
    seed: Item | None
    iron_depot: auto
    manual_fishing: auto
    runecube: auto
    silver_per_hit: auto
    xp_per_hit: auto

    items: list["DropRatesItem"]


@strawberry.django.type(models.DropRatesItem)
class DropRatesItem:
    drop_rates: DropRates
    item: Item
    rate: auto
