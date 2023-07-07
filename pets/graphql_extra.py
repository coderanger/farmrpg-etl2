import strawberry
from strawberry import auto

from . import models


@strawberry.django.order(models.Pet)
class PetOrder:
    id: auto
    name: auto


@strawberry.django.order(models.PetItem)
class PetItemOrder:
    level: auto
    pet: PetOrder
