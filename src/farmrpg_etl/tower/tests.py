import json
from pathlib import Path

import httpx
import pytest
from asgiref.sync import async_to_sync

from ..items.factories import ItemFactory
from .models import TowerReward
from .parsers import ParsedTowerReward, parse_tower_txt
from .tasks import scrape_all_from_api

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def tower() -> bytes:
    return FIXTURES_ROOT.joinpath("tower.txt").open("r").read()


@pytest.fixture
def tower_json() -> dict:
    return json.load(FIXTURES_ROOT.joinpath("tower.json").open("r"))


def test_parse_tower_txt(tower: str):
    tower = list(parse_tower_txt(tower))
    assert len(tower) == 199 * 3
    assert tower[0] == ParsedTowerReward(
        level=199, order=1, item="Ancient Coin", quantity=1900
    )
    assert tower[2] == ParsedTowerReward(
        level=199, order=3, item="Piece of Heart", quantity=1
    )
    assert tower[596] == ParsedTowerReward(level=1, order=3, item="Gold", quantity=100)


@pytest.mark.django_db
def test_scrape_from_api(tower_json: dict, respx_mock):
    # Create items as needed.
    items_created = set[int]()
    for row in tower_json["tower_levels"]:
        for i in range(1, 4):
            if row[f"item{i}"] != 0 and row[f"item{i}"] not in items_created:
                ItemFactory(id=row[f"item{i}"])
                items_created.add(row[f"item{i}"])

    respx_mock.get("https://farmrpg.com/api.php?method=tower").mock(
        return_value=httpx.Response(200, json=tower_json)
    )
    async_to_sync(scrape_all_from_api)()
    trs = TowerReward.objects.all()
    assert len(trs) == 907
    assert trs[0].level == 300
    assert trs[0].item_id == 752
    assert trs[0].item_quantity == 10
    assert trs[500].level == 136
    assert trs[500].item_id == 249
    assert trs[500].item_quantity == 1300
