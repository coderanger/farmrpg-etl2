import strawberry
from strawberry import auto

from items.graphql import Item

from . import models


@strawberry.django.filter(models.Quiz)
class QuizFilter:
    id: auto
    name: auto


@strawberry.django.type(models.Quiz, filters=QuizFilter)
class Quiz:
    id: int
    name: auto
    description: auto

    rewards: list["QuizReward"]
    answers: list["QuizAnswer"]


@strawberry.django.type(models.QuizReward)
class QuizReward:
    quiz: Quiz
    score: auto
    item: Item
    quantity: auto


@strawberry.django.type(models.QuizAnswer)
class QuizAnswer:
    quiz: Quiz
    display_order: auto
    question: auto
    answer1: auto
    answer2: auto
    answer3: auto
    answer4: auto
    correct: auto
