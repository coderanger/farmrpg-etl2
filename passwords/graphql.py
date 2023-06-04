from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto
from django.db.models import QuerySet

from items.graphql import Item

from . import models


@gql.django.filters.filter(models.PasswordGroup)
class PasswordGroupFilter:
    name: auto


@gql.django.type(models.PasswordGroup, filters=PasswordGroupFilter)
class PasswordGroup:
    name: auto
    passwords: list["Password"]


@gql.django.filters.filter(models.Password)
class PasswordFilter:
    id: int
    password: auto
    has_clues: bool

    def filter_has_clues(
        self, queryset: QuerySet[models.Password]
    ) -> QuerySet[models.Password]:
        if self.has_clues:
            return queryset.exclude(clue1=None, clue2=None, clue3=None)
        return queryset


@gql.django.type(models.Password, filters=PasswordFilter)
class Password:
    id: int
    group: PasswordGroup
    password: auto
    clue1: auto
    clue2: auto
    clue3: auto

    reward_silver: auto
    reward_gold: auto
    reward_items: list["PasswordItem"]


@gql.django.type(models.PasswordItem)
class PasswordItem:
    password: Password
    item: Item
    quantity: auto
