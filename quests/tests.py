from datetime import datetime, timezone

import httpx
import pytest
from asgiref.sync import async_to_sync

from items.factories import ItemFactory

from .models import (
    Quest,
    QuestEvent,
    QuestItemRequired,
    QuestItemRequiredEvent,
    QuestItemReward,
    QuestItemRewardEvent,
)
from .tasks import scrape_all_from_api
from .html_sanitizer import sanitize_quest_description


@pytest.fixture
def item1():
    return ItemFactory(id=1)


@pytest.fixture
def item2():
    return ItemFactory(id=2)


@pytest.mark.django_db
def test_quest_scrape(respx_mock, item1, item2):
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 2768520,
                    "npc": "Borgen",
                    "title": "Blooming Thaw Already IV",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "2023-05-31",
                    "main_quest": 0,
                    "start_date": "2023-03-01",
                    "description": "Since the weather is still too cold for the ...",
                    "reward_gold": 0,
                    "reward_items": "1|5",
                    "reward_silver": 0,
                    "required_items": "2|10",
                    "completed_count": 2038,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 20,
                    "required_fishing_level": 20,
                    "required_crafting_level": 20,
                    "required_exploring_level": 20,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    num_quests = Quest.objects.all().count()
    assert num_quests == 1
    quest = Quest.objects.get()
    assert quest.npc == "Borgen"
    assert quest.title == "Blooming Thaw Already IV"
    assert quest.pred is None
    assert quest.start_date == datetime(2023, 3, 1, 6, tzinfo=timezone.utc)
    assert quest.end_date == datetime(2023, 6, 1, 4, 59, 59, tzinfo=timezone.utc)
    assert quest.main_quest is False
    assert quest.author is None
    assert quest.required_items.count() == 1
    assert quest.required_items.get().item.name == "Item 2"
    assert quest.required_items.get().quantity == 10
    assert quest.reward_items.count() == 1
    assert quest.reward_items.get().item.name == "Item 1"
    assert quest.reward_items.get().quantity == 5


@pytest.mark.django_db
def test_quest_scrape_no_update(respx_mock, item1, item2):
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 2768520,
                    "npc": "Borgen",
                    "npc_img": "",
                    "title": "Blooming Thaw Already IV",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "2023-05-31",
                    "main_quest": 0,
                    "start_date": "2023-03-01",
                    "description": "Since the weather is still too cold for the ...",
                    "reward_gold": 0,
                    "reward_items": "1|5",
                    "reward_silver": 0,
                    "required_items": "2|10",
                    "completed_count": 2038,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 20,
                    "required_fishing_level": 20,
                    "required_crafting_level": 20,
                    "required_exploring_level": 20,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    assert Quest.objects.count() == 1
    assert QuestEvent.objects.count() == 1
    assert QuestItemRequired.objects.count() == 1
    assert QuestItemRequiredEvent.objects.count() == 1
    assert QuestItemReward.objects.count() == 1
    assert QuestItemRewardEvent.objects.count() == 1
    async_to_sync(scrape_all_from_api)()
    assert Quest.objects.count() == 1
    assert QuestEvent.objects.count() == 1
    assert QuestItemRequired.objects.count() == 1
    assert QuestItemRequiredEvent.objects.count() == 1
    assert QuestItemReward.objects.count() == 1
    assert QuestItemRewardEvent.objects.count() == 1


@pytest.mark.django_db
def test_quest_scrape_update(respx_mock, item1, item2):
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 2768520,
                    "npc": "Borgen",
                    "npc_img": "",
                    "title": "Blooming Thaw Already IV",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "2023-05-31",
                    "main_quest": 0,
                    "start_date": "2023-03-01",
                    "description": "Since the weather is still too cold for the ...",
                    "reward_gold": 0,
                    "reward_items": "1|5",
                    "reward_silver": 0,
                    "required_items": "2|10",
                    "completed_count": 2038,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 20,
                    "required_fishing_level": 20,
                    "required_crafting_level": 20,
                    "required_exploring_level": 20,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    assert Quest.objects.count() == 1
    assert QuestEvent.objects.count() == 1
    assert QuestItemRequired.objects.count() == 1
    assert QuestItemRequiredEvent.objects.count() == 1
    assert QuestItemReward.objects.count() == 1
    assert QuestItemRewardEvent.objects.count() == 1
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 2768520,
                    "npc": "Borgen",
                    "npc_img": "",
                    "title": "Blooming Thaw Already IV Updated",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "2023-05-31",
                    "main_quest": 0,
                    "start_date": "2023-03-01",
                    "description": "Since the weather is still too cold for the ...",
                    "reward_gold": 0,
                    "reward_items": "1|5",
                    "reward_silver": 0,
                    "required_items": "1|10",
                    "completed_count": 2038,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 20,
                    "required_fishing_level": 20,
                    "required_crafting_level": 20,
                    "required_exploring_level": 20,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    assert Quest.objects.count() == 1
    assert QuestEvent.objects.count() == 2
    assert QuestItemRequired.objects.count() == 1
    assert QuestItemRequiredEvent.objects.count() == 2
    assert QuestItemReward.objects.count() == 1
    assert QuestItemRewardEvent.objects.count() == 1


@pytest.mark.django_db
def test_quest_scrape_no_dated(respx_mock, item1, item2):
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 2768520,
                    "npc": "Borgen",
                    "npc_img": "",
                    "title": "Blooming Thaw Already IV",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "0000-00-00",
                    "main_quest": 0,
                    "start_date": "0000-00-00",
                    "description": "Since the weather is still too cold for the ...",
                    "reward_gold": 0,
                    "reward_items": "1|5",
                    "reward_silver": 0,
                    "required_items": "2|10",
                    "completed_count": 2038,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 20,
                    "required_fishing_level": 20,
                    "required_crafting_level": 20,
                    "required_exploring_level": 20,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    quest = Quest.objects.get()
    assert quest.start_date is None
    assert quest.end_date is None


@pytest.mark.django_db
def test_quest_scrape_pred(respx_mock, item1, item2):
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 533,
                    "npc": "George",
                    "npc_img": "",
                    "title": "99 Bottles XLVIII",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "0000-00-00",
                    "main_quest": 0,
                    "start_date": "0000-00-00",
                    "description": "Forty-Eight bottles of hops on the wall...",
                    "reward_gold": 0,
                    "reward_items": "",
                    "reward_silver": 14400,
                    "required_items": "",
                    "completed_count": 19913,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 48,
                    "required_fishing_level": 0,
                    "required_crafting_level": 48,
                    "required_exploring_level": 0,
                },
                {
                    "id": 522,
                    "npc": "George",
                    "npc_img": "",
                    "title": "99 Bottles XXXVII",
                    "author": "",
                    "pred_id": 533,
                    "end_date": "0000-00-00",
                    "main_quest": 0,
                    "start_date": "0000-00-00",
                    "description": "Thirty-Seven bottles of hops on the wall...",
                    "reward_gold": 0,
                    "reward_items": "",
                    "reward_silver": 11100,
                    "required_items": "",
                    "completed_count": 21757,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 37,
                    "required_fishing_level": 0,
                    "required_crafting_level": 37,
                    "required_exploring_level": 0,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    quest1 = Quest.objects.get(id=533)
    assert quest1.pred is None
    quest2 = Quest.objects.get(id=522)
    assert quest2.pred_id == 533
    assert quest2.pred.title == "99 Bottles XLVIII"


@pytest.mark.django_db
def test_quest_scrape_pred_backwards(respx_mock, item1, item2):
    respx_mock.get("https://farmrpg.com/api/quests/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 522,
                    "npc": "George",
                    "npc_img": "",
                    "title": "99 Bottles XXXVII",
                    "author": "",
                    "pred_id": 533,
                    "end_date": "0000-00-00",
                    "main_quest": 0,
                    "start_date": "0000-00-00",
                    "description": "Thirty-Seven bottles of hops on the wall...",
                    "reward_gold": 0,
                    "reward_items": "",
                    "reward_silver": 11100,
                    "required_items": "",
                    "completed_count": 21757,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 37,
                    "required_fishing_level": 0,
                    "required_crafting_level": 37,
                    "required_exploring_level": 0,
                },
                {
                    "id": 533,
                    "npc": "George",
                    "npc_img": "",
                    "title": "99 Bottles XLVIII",
                    "author": "",
                    "pred_id": 0,
                    "end_date": "0000-00-00",
                    "main_quest": 0,
                    "start_date": "0000-00-00",
                    "description": "Forty-Eight bottles of hops on the wall...",
                    "reward_gold": 0,
                    "reward_items": "",
                    "reward_silver": 14400,
                    "required_items": "",
                    "completed_count": 19913,
                    "required_npc_id": 0,
                    "required_silver": 0,
                    "required_npc_level": 0,
                    "required_tower_level": 0,
                    "required_cooking_level": 0,
                    "required_farming_level": 48,
                    "required_fishing_level": 0,
                    "required_crafting_level": 48,
                    "required_exploring_level": 0,
                },
            ],
        )
    )
    async_to_sync(scrape_all_from_api)()
    quest1 = Quest.objects.get(id=533)
    assert quest1.pred is None
    quest2 = Quest.objects.get(id=522)
    assert quest2.pred_id == 533
    assert quest2.pred.title == "99 Bottles XLVIII"


def test_sanitize_quest_description_489778():
    description = 'Buddy has been so happy since you repaired his peg leg. A few days have passed, and he knocks on your door. <br><br>"Hi best friend! Best friends give each other things, right? I have some things I want to give you! Do you have any things for me?"\r\n<br><br><marquee direction="down" width="400" height="100" behavior="alternate"><marquee behavior="alternate"><font size = "5"><font color="mediumseagreen">:D BEST FRIENDS FOREVER :D</font color></font size></marquee></marquee><br><br><br><br>'  # noqa: E501
    assert (
        sanitize_quest_description(description)
        == 'Buddy has been so happy since you repaired his peg leg. A few days have passed, and he knocks on your door. <br><br>"Hi best friend! Best friends give each other things, right? I have some things I want to give you! Do you have any things for me?"\r\n<br><br><font size="5">:D BEST FRIENDS FOREVER :D</font>'  # noqa: E501
    )
