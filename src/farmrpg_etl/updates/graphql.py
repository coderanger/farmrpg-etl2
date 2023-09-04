from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from . import models


@gql.django.filters.filter(models.Update)
class UpdateFilter:
    date: auto


@gql.django.type(models.Update, filters=UpdateFilter)
class Update:
    date: auto
    content: auto
    clean_content: auto
    text_content: auto
