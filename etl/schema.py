import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from borgen.graphql import BorgenItem
from chat.graphql import Emblem
from community_center.graphql import CommunityCenter
from exchange_center.graphql import CardsTrade, Trade
from items.graphql import Item, SkillLevelReward
from locations.graphql import Location
from npcs.graphql import NPC
from passwords.graphql import Password, PasswordGroup
from pbgs.graphql import ProfileBackground
from pets.graphql import Pet
from quests.graphql import Quest, Questline
from quizzes.graphql import Quiz
from tower.graphql import TowerReward
from updates.graphql import Update


@strawberry.type
class Query:
    items: list[Item] = strawberry.django.field()
    quests: list[Quest] = strawberry.django.field()
    questlines: list[Questline] = strawberry.django.field()
    pets: list[Pet] = strawberry.django.field()
    locations: list[Location] = strawberry.django.field()
    quizzes: list[Quiz] = strawberry.django.field()
    emblems: list[Emblem] = strawberry.django.field()
    npcs: list[NPC] = strawberry.django.field()
    updates: list[Update] = strawberry.django.field()
    trades: list[Trade] = strawberry.django.field()
    cards_trades: list[CardsTrade] = strawberry.django.field()
    borgen_items: list[BorgenItem] = strawberry.django.field()
    community_centers: list[CommunityCenter] = strawberry.django.field()
    profile_backgrounds: list[ProfileBackground] = strawberry.django.field()
    tower_rewards: list[TowerReward] = strawberry.django.field()
    skill_level_rewards: list[SkillLevelReward] = strawberry.django.field()
    password_groups: list[PasswordGroup] = strawberry.django.field()
    passwords: list[Password] = strawberry.django.field()


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
