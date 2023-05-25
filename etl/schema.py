from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from chat.graphql import Emblem
from items.graphql import Item
from locations.graphql import Location
from npcs.graphql import NPC
from pets.graphql import Pet
from quests.graphql import Quest
from quizzes.graphql import Quiz
from updates.graphql import Update
from exchange_center.graphql import Trade
from borgen.graphql import BorgenItem
from community_center.graphql import CommunityCenter


@gql.type
class Query:
    items: list[Item] = gql.django.field()
    quests: list[Quest] = gql.django.field()
    pets: list[Pet] = gql.django.field()
    locations: list[Location] = gql.django.field()
    quizzes: list[Quiz] = gql.django.field()
    emblems: list[Emblem] = gql.django.field()
    npcs: list[NPC] = gql.django.field()
    updates: list[Update] = gql.django.field()
    trades: list[Trade] = gql.django.field()
    borgen_items: list[BorgenItem] = gql.django.field()
    community_centers: list[CommunityCenter] = gql.django.field()


schema = gql.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
