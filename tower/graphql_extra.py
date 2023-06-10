from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto


from . import models


@gql.django.ordering.order(models.TowerReward)
class TowerRewardOrder:
    level: auto
    order: auto
