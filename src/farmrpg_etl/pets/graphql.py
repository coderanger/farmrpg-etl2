from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from ..items.graphql import Item

from . import models
from .graphql_extra import PetItemOrder, PetOrder


@gql.django.filters.filter(models.Pet)
class PetFilter:
    id: auto
    name: auto


@gql.django.type(models.Pet, filters=PetFilter, order=PetOrder)
class Pet:
    id: int = gql.field(resolver=lambda self: self.game_id)
    name: auto
    image: auto
    cost: float

    required_farming_level: auto
    required_fishing_level: auto
    required_crafting_level: auto
    required_exploring_level: auto

    pet_items: list["PetItem"]


@gql.django.type(models.PetItem, order=PetItemOrder)
class PetItem:
    id: int
    pet: Pet
    item: Item
    level: auto
