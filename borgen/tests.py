from pathlib import Path

import pytest

from .parsers import parse_borgens, ParsedItem

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def tent() -> bytes:
    return FIXTURES_ROOT.joinpath("tent.html").open("rb").read()


@pytest.fixture
def tent2() -> bytes:
    return FIXTURES_ROOT.joinpath("tent2.html").open("rb").read()


def test_parse_borgens(tent: bytes):
    assert list(parse_borgens(tent)) == [
        ParsedItem(item=103, price=1),
        ParsedItem(item=120, price=4),
        ParsedItem(item=84, price=6),
        ParsedItem(item=251, price=10),
        ParsedItem(item=250, price=25),
        ParsedItem(item=263, price=50),
        ParsedItem(item=153, price=100),
    ]


def test_parse_borgens2(tent2: bytes):
    assert list(parse_borgens(tent2)) == [
        ParsedItem(item=103, price=None),
        ParsedItem(item=120, price=4),
        ParsedItem(item=84, price=6),
        ParsedItem(item=251, price=10),
        ParsedItem(item=250, price=25),
        ParsedItem(item=263, price=50),
        ParsedItem(item=153, price=100),
    ]
