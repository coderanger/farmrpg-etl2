from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto


from . import models


@gql.django.ordering.order(models.Pet)
class PetOrder:
    id: auto
    name: auto


@gql.django.ordering.order(models.PetItem)
class PetItemOrder:
    level: auto
    pet: PetOrder
