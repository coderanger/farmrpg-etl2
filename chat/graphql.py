from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from . import models


@gql.django.filters.filter(models.Emblem)
class EmblemFilter:
    id: auto
    type: auto
    name: auto
    keywords: auto


@gql.django.type(models.Emblem, filters=EmblemFilter)
class Emblem:
    id: int
    name: auto
    image: auto
    type: auto
    keywords: auto
    created_at: auto
