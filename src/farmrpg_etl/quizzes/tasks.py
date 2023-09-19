from collections import defaultdict

import structlog

from ..items.models import Item
from ..utils.http import client
from .models import Quiz, QuizAnswer, QuizReward

log = structlog.stdlib.get_logger(mod=__name__)


async def update_quiz_reward(quiz_id: int, score: int, item_name: str, quantity: int):
    item_id = (
        await Item.objects.filter(name=item_name).values_list("id", flat=True).aget()
    )
    await QuizReward.objects.aupdate_or_create(
        quiz_id=quiz_id, score=score, item_id=item_id, quantity=quantity
    )


async def scrape_quizzes_from_api():
    resp = await client.get("/api/quizzes/")
    resp.raise_for_status()
    data = resp.json()

    for row in data:
        await Quiz.objects.aupdate_or_create(
            id=row["id"],
            defaults={"name": row["name"], "description": row["description"]},
        )
        await update_quiz_reward(row["id"], 80, row["score80reward"], row["score80amt"])
        await update_quiz_reward(row["id"], 90, row["score90reward"], row["score90amt"])
        await update_quiz_reward(
            row["id"], 100, row["score100reward"], row["score100amt"]
        )


def _sanitize_text(val: str | None) -> str | None:
    if val is None:
        return None
    return val.replace("<br/>", "")


async def scrape_answers_from_api():
    resp = await client.get("/api/answers/")
    resp.raise_for_status()
    data = resp.json()

    seen_orders = defaultdict(list)

    for row in data:
        await QuizAnswer.objects.aupdate_or_create(
            quiz_id=row["quiz_id"],
            display_order=row["display_order"],
            defaults={
                "question": _sanitize_text(row["question"]),
                "answer1": _sanitize_text(row["answer1"]),
                "answer2": _sanitize_text(row["answer2"]),
                "answer3": _sanitize_text(row["answer3"]),
                "answer4": _sanitize_text(row["answer4"]),
                "correct": row["correct"],
            },
        )
        seen_orders[row["quiz_id"]].append(row["display_order"])

    for quiz_id, seen in seen_orders.items():
        await QuizAnswer.objects.filter(quiz_id=quiz_id).exclude(
            display_order__in=seen
        ).adelete()


async def scrape_all_from_api():
    await scrape_quizzes_from_api()
    await scrape_answers_from_api()
