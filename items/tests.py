from pathlib import Path

import pytest

from .parsers import parse_item, ParsedIngredient

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
