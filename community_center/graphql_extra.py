import strawberry
from strawberry import auto

from . import models


@strawberry.django.order(models.CommunityCenter)
class CommunityCenterOrder:
    id: auto
    date: auto
