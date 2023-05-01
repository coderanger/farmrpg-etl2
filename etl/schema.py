from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from items.graphql import Item
from pets.graphql import Pet
from quests.graphql import Quest


@gql.type
class Query:
    items: list[Item] = gql.django.field()
    quests: list[Quest] = gql.django.field()
    pets: list[Pet] = gql.django.field()


schema = gql.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
