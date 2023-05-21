from pathlib import Path

import pytest

from .parsers import parse_exchange_center, ParsedTrade

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def exchange() -> bytes:
    return FIXTURES_ROOT.joinpath("exchange.html").open("rb").read()


def test_parse_exchange_center(exchange: bytes):
    trades = list(parse_exchange_center(exchange))
    assert trades == [
        ParsedTrade(
            input_item=111,
            input_quantity=500,
            output_item=508,
            output_quantity=5,
            oneshot=False,
        ),
        ParsedTrade(
            input_item=113,
            input_quantity=1000,
            output_item=268,
            output_quantity=10,
            oneshot=False,
        ),
        ParsedTrade(
            input_item=237,
            input_quantity=400,
            output_item=505,
            output_quantity=3,
            oneshot=False,
        ),
        ParsedTrade(
            input_item=314,
            input_quantity=500,
            output_item=491,
            output_quantity=25,
            oneshot=False,
        ),
        ParsedTrade(
            input_item=335,
            input_quantity=500,
            output_item=347,
            output_quantity=25,
            oneshot=False,
        ),
    ]
