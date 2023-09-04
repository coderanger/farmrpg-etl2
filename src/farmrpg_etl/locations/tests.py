from pathlib import Path

import pytest

from .parser import parse_location, parse_locations

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def misty_forest() -> bytes:
    return FIXTURES_ROOT.joinpath("misty_forest.html").open("rb").read()


@pytest.fixture
def locations() -> bytes:
    return FIXTURES_ROOT.joinpath("locations.html").open("rb").read()


def test_parse_location(misty_forest: bytes):
    assert parse_location(misty_forest) == {
        "name": "Misty Forest",
        "image": "/img/items/mistforest.png",
        "items": [
            35,
            43,
            52,
            91,
            92,
            93,
            128,
            151,
            171,
            172,
            187,
            188,
            244,
            282,
            289,
            362,
            479,
        ],
    }


def test_parse_locations(locations: bytes):
    assert list(parse_locations(locations)) == [
        ("fishing", 1),
        ("fishing", 2),
        ("fishing", 3),
        ("fishing", 4),
        ("fishing", 5),
        ("fishing", 6),
        ("fishing", 7),
        ("fishing", 8),
        ("fishing", 9),
        ("fishing", 10),
        ("fishing", 11),
        ("fishing", 12),
        ("explore", 1),
        ("explore", 7),
        ("explore", 2),
        ("explore", 3),
        ("explore", 4),
        ("explore", 5),
        ("explore", 6),
        ("explore", 8),
        ("explore", 9),
        ("explore", 10),
        ("explore", 13),
    ]
