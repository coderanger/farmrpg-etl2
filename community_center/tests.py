import datetime
from pathlib import Path

import pytest

from .parsers import ParsedCommunityCenter, parse_community_center

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def comm() -> bytes:
    return FIXTURES_ROOT.joinpath("comm.html").open("rb").read()


def test_parse_community_center(comm: bytes):
    assert list(parse_community_center(comm, today=datetime.date(2023, 7, 10))) == [
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 10),
            input_item=43,
            input_item_name="Mushroom",
            input_quantity=2_754_400,
            output_item=382,
            output_quantity=40,
            progress=1_663_146,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 9),
            input_item=None,
            input_item_name="Starfish",
            input_quantity=1_367_100,
            output_item=339,
            output_quantity=10,
            progress=7_464_756,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 8),
            input_item=None,
            input_item_name="Gummy Worms",
            input_quantity=6_823_900,
            output_item=347,
            output_quantity=5,
            progress=11_301_007,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 7),
            input_item=None,
            input_item_name="Caterpillar",
            input_quantity=2_261_900,
            output_item=84,
            output_quantity=100,
            progress=2_516_158,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 6),
            input_item=None,
            input_item_name="Purple Diary",
            input_quantity=1_003_000,
            output_item=172,
            output_quantity=10,
            progress=1_856_956,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 5),
            input_item=None,
            input_item_name="Hot Potato",
            input_quantity=125_000,
            output_item=761,
            output_quantity=1,
            progress=151_916,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 4),
            input_item=None,
            input_item_name="Hot Potato",
            input_quantity=125_000,
            output_item=781,
            output_quantity=1,
            progress=153_286,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 7, 3),
            input_item=None,
            input_item_name="Hot Potato",
            input_quantity=125_000,
            output_item=778,
            output_quantity=1,
            progress=153_616,
        ),
    ]
