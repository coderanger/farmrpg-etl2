import json
from pathlib import Path

import httpx
import pytest
from asgiref.sync import async_to_sync

from .models import Item
from .parsers import ParsedIngredient, parse_item
from .tasks import scrape_items

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def scissors() -> bytes:
    return FIXTURES_ROOT.joinpath("item_scissors.html").open("rb").read()


@pytest.fixture
def mc02() -> bytes:
    return FIXTURES_ROOT.joinpath("item_mystical_chest_02.html").open("rb").read()


@pytest.fixture
def cornucopia() -> bytes:
    return FIXTURES_ROOT.joinpath("item_cornucopia.html").open("rb").read()


@pytest.fixture
def gb02() -> bytes:
    return FIXTURES_ROOT.joinpath("item_grab_bag_02.html").open("rb").read()


@pytest.fixture
def snowball() -> bytes:
    return FIXTURES_ROOT.joinpath("item_snowball.html").open("rb").read()


@pytest.fixture
def items() -> dict:
    return json.load(FIXTURES_ROOT.joinpath("items").open("r"))

def test_parse_recipe(scissors: bytes):
    item = parse_item(scissors)
    assert item.recipe == [
        ParsedIngredient(id=95, quantity=1),
        ParsedIngredient(id=38, quantity=1),
        ParsedIngredient(id=145, quantity=2),
        ParsedIngredient(id=40, quantity=1),
        ParsedIngredient(id=35, quantity=2),
    ]
    assert item.locksmith == []
    assert item.flea_market_price is None
    assert item.from_event is False


def test_parse_locksmith(mc02: bytes):
    item = parse_item(mc02)
    assert item.recipe == []
    assert item.locksmith == [
        ParsedIngredient(id=350, quantity=3),
        ParsedIngredient(id=500, quantity=3),
        ParsedIngredient(id=538, quantity=3),
        ParsedIngredient(id=266, quantity=1),
        ParsedIngredient(id=373, quantity=2),
    ]


def test_parse_locksmith_gold(cornucopia: bytes):
    item = parse_item(cornucopia)
    assert item.recipe == []
    assert item.locksmith[0] == ParsedIngredient(id=0, gold=True, quantity=25)


def test_parse_fleamarket(gb02: bytes):
    item = parse_item(gb02)
    assert item.flea_market_price == 4


def test_parse_event(snowball: bytes):
    item = parse_item(snowball)
    assert item.from_event is True


@pytest.mark.django_db
def test_scrape_from_api_grape_pie(items: dict, respx_mock):
    respx_mock.get("https://farmrpg.com/api.php?method=items").mock(
        return_value=httpx.Response(200, json=items)
    )
    async_to_sync(scrape_items)()
    item = Item.objects.get(id=726)
    assert item.cooking_recipe_item.name == "Rosalie's Concord Grape Pie"
