import strawberry
from strawberry import auto

from items.graphql import Item

from . import models
from .graphql_extra import PetItemOrder, PetOrder


@strawberry.django.filter(models.Pet)
class PetFilter:
    game_id: auto
    name: auto


@strawberry.django.type(models.Pet, filters=PetFilter, order=PetOrder)
class Pet:
    game_id: int
    name: auto
    image: auto
    cost: float

    required_farming_level: auto
    required_fishing_level: auto
    required_crafting_level: auto
    required_exploring_level: auto

    pet_items: list["PetItem"]


@strawberry.django.type(models.PetItem, order=PetItemOrder)
class PetItem:
    id: int
    pet: Pet
    item: Item
    level: auto
