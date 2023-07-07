import strawberry
from strawberry import auto

from . import models


@strawberry.django.filter(models.Update)
class UpdateFilter:
    date: auto


@strawberry.django.type(models.Update, filters=UpdateFilter)
class Update:
    date: auto
    content: auto
    clean_content: auto
    text_content: auto
