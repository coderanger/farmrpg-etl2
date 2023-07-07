import strawberry
from django.db.models import QuerySet
from strawberry import auto

from items.graphql import Item

from . import models


@strawberry.django.filter(models.PasswordGroup)
class PasswordGroupFilter:
    name: auto


@strawberry.django.type(models.PasswordGroup, filters=PasswordGroupFilter)
class PasswordGroup:
    name: auto
    passwords: list["Password"]


@strawberry.django.filter(models.Password)
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


@strawberry.django.type(models.Password, filters=PasswordFilter)
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


@strawberry.django.type(models.PasswordItem)
class PasswordItem:
    password: Password
    item: Item
    quantity: auto
