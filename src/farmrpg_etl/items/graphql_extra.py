from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from . import models


@gql.django.filters.filter(models.Item)
class ItemFilter:
    id: auto
    name: auto
    can_mail: auto


@gql.django.ordering.order(models.Item)
class ItemOrder:
    id: auto
    name: auto
    created_at: auto
