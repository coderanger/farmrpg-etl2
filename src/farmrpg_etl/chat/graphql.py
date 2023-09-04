from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto
from django.db.models import QuerySet

from . import models


@gql.django.filters.filter(models.Emblem)
class EmblemFilter:
    id: auto
    type: auto
    name: auto
    keywords: auto
    non_staff: bool | None

    def filter_non_staff(self, queryset: QuerySet[models.Emblem]) -> QuerySet[models.Emblem]:
        if self.non_staff:
            return queryset.exclude(type="staff")
        return queryset


@gql.django.type(models.Emblem, filters=EmblemFilter)
class Emblem:
    id: int
    name: auto
    image: auto
    type: auto
    keywords: auto
    created_at: auto
