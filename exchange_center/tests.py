from pathlib import Path

import pytest

from .parsers import parse_exchange_center, ParsedTrade, parse_cards, ParsedCardTrade

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def exchange() -> bytes:
    return FIXTURES_ROOT.joinpath("exchange.html").open("rb").read()


@pytest.fixture
def cards() -> bytes:
    return FIXTURES_ROOT.joinpath("cards.html").open("rb").read()


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


def test_parse_cards(cards: bytes):
    card_trades = list(parse_cards(cards))
    assert card_trades == [
        ParsedCardTrade(
            id=1,
            spades_quantity=1,
            hearts_quantity=1,
            diamonds_quantity=1,
            clubs_quantity=1,
            joker_quantity=None,
            output_item="Borgen Buck",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=2,
            spades_quantity=None,
            hearts_quantity=None,
            diamonds_quantity=None,
            clubs_quantity=4,
            joker_quantity=None,
            output_item="Piece 11",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=3,
            spades_quantity=2,
            hearts_quantity=None,
            diamonds_quantity=3,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Mega Cotton Seeds",
            output_quantity=50,
        ),
        ParsedCardTrade(
            id=4,
            spades_quantity=None,
            hearts_quantity=4,
            diamonds_quantity=None,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Lovely Cookies",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=5,
            spades_quantity=None,
            hearts_quantity=None,
            diamonds_quantity=2,
            clubs_quantity=3,
            joker_quantity=None,
            output_item="Runestone Necklace",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=6,
            spades_quantity=2,
            hearts_quantity=2,
            diamonds_quantity=None,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Arnold Palmer",
            output_quantity=300,
        ),
        ParsedCardTrade(
            id=7,
            spades_quantity=4,
            hearts_quantity=None,
            diamonds_quantity=None,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Large Net",
            output_quantity=500,
        ),
        ParsedCardTrade(
            id=8,
            spades_quantity=None,
            hearts_quantity=2,
            diamonds_quantity=None,
            clubs_quantity=3,
            joker_quantity=None,
            output_item="Raptor Claw",
            output_quantity=10,
        ),
        ParsedCardTrade(
            id=9,
            spades_quantity=None,
            hearts_quantity=None,
            diamonds_quantity=None,
            clubs_quantity=None,
            joker_quantity=4,
            output_item="Buddy Doll",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=10,
            spades_quantity=None,
            hearts_quantity=3,
            diamonds_quantity=2,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Piece of Heart",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=11,
            spades_quantity=4,
            hearts_quantity=None,
            diamonds_quantity=None,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Spooky Cookies",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=12,
            spades_quantity=1,
            hearts_quantity=1,
            diamonds_quantity=1,
            clubs_quantity=1,
            joker_quantity=None,
            output_item="Joker",
            output_quantity=1,
        ),
        ParsedCardTrade(
            id=13,
            spades_quantity=3,
            hearts_quantity=None,
            diamonds_quantity=2,
            clubs_quantity=None,
            joker_quantity=None,
            output_item="Honeycomb",
            output_quantity=1,
        ),
    ]
