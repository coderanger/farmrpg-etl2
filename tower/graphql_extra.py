import strawberry
from strawberry import auto

from . import models


@strawberry.django.order(models.TowerReward)
class TowerRewardOrder:
    level: auto
    order: auto
