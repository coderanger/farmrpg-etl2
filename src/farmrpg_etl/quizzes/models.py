import datetime

import pghistory
from django.db import models
from django.utils import timezone

from ..items.models import Item

# The interval at which quiz answers become visible.
ANSWER_REVEAL_THRESHOLD = datetime.timedelta(days=1)


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Quiz(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "quizzes"

    def __str__(self) -> str:
        return self.name


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class QuizReward(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="rewards")
    score = models.IntegerField()
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="quiz_rewards"
    )
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "score"],
                name="quiz_score",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.quiz.name} - {self.score}"


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class QuizAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    display_order = models.IntegerField()
    question = models.TextField()
    answer1 = models.TextField(blank=True)
    answer2 = models.TextField(blank=True)
    answer3 = models.TextField(blank=True)
    answer4 = models.TextField(blank=True)
    correct = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "display_order"],
                name="quiz_display_order",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.quiz.name} - {self.display_order}"

    @property
    def is_hidden(self) -> bool:
        return (timezone.now() - self.created_at) < ANSWER_REVEAL_THRESHOLD
