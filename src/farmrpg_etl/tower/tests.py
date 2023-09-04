from pathlib import Path

import pytest

from .parsers import parse_tower_txt, ParsedTowerReward

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def tower() -> bytes:
    return FIXTURES_ROOT.joinpath("tower.txt").open("r").read()


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
