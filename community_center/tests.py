import datetime
from pathlib import Path

import pytest

from .parsers import parse_community_center, ParsedCommunityCenter

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def comm() -> bytes:
    return FIXTURES_ROOT.joinpath("comm.html").open("rb").read()


def test_parse_community_center(comm: bytes):
    assert list(parse_community_center(comm, today=datetime.date(2023, 5, 23))) == [
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 23),
            input_item=63,
            input_item_name="Trout",
            input_quantity=6_142_100,
            output_item=144,
            output_quantity=100,
            progress=3_232_503,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 22),
            input_item=None,
            input_item_name="Bacon",
            input_quantity=722_200,
            output_item=347,
            output_quantity=5,
            progress=833_845,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 21),
            input_item=None,
            input_item_name="Aquamarine",
            input_quantity=1_605_600,
            output_item=84,
            output_quantity=100,
            progress=2_337_445,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 20),
            input_item=None,
            input_item_name="Bucket",
            input_quantity=2_564_000,
            output_item=459,
            output_quantity=10,
            progress=3_600_074,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 19),
            input_item=None,
            input_item_name="4-leaf Clover",
            input_quantity=1_740_300,
            output_item=250,
            output_quantity=7,
            progress=3_427_890,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 18),
            input_item=None,
            input_item_name="Spider",
            input_quantity=1_547_500,
            output_item=157,
            output_quantity=50,
            progress=675_349,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 17),
            input_item=None,
            input_item_name="Drum",
            input_quantity=5_126_200,
            output_item=194,
            output_quantity=100,
            progress=7_273_661,
        ),
        ParsedCommunityCenter(
            date=datetime.date(2023, 5, 16),
            input_item=None,
            input_item_name="Mushroom",
            input_quantity=2_754_400,
            output_item=363,
            output_quantity=3,
            progress=3_216_461,
        ),
    ]
