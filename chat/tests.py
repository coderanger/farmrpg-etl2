from pathlib import Path

import pytest

from .parsers import parse_emblems

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def settings() -> bytes:
    return FIXTURES_ROOT.joinpath("settings.html").open("rb").read()


def test_parse_emblems(settings: bytes):
    ems = list(parse_emblems(settings))
    assert len(ems) == 577
    assert ems[0] == {
        "id": 3,
        "image": "img/emblems/emblem_clover01.png",
        "keywords": "4 leaf clover,green, plant",
        "name": "Emblem Clover 01",
        "type": None,
    }
    assert ems[8] == {
        "id": 620,
        "image": "img/emblems/2DB9B8C9-5D9F-4947-9BBE-428A8016B6EC.png",
        "keywords": "Another Duck In The Wall,Duck",
        "name": "Another Duck In The Wall",
        "type": None,
    }
    assert ems[100] == {
        "id": 118,
        "image": "img/emblems/YellowCornJail96.png",
        "keywords": "Corn Jail,",
        "name": "Yellow Corn Jail",
        "type": None,
    }
    assert ems[400] == {
        "id": 319,
        "image": "img/emblems/SturdySword96.png",
        "keywords": "Sturdy Sword,item, sturdy, sword",
        "name": "Sturdy Sword",
        "type": None,
    }
    assert ems[500] == {
        "id": 48,
        "image": "img/emblems/FishJelly96.png",
        "keywords": "Jelly Fish,Fish, jelly, jar",
        "name": "Fish Jelly",
        "type": "patreon",
    }
    assert ems[541] == {
        "id": 126,
        "image": "img/emblems/APath96.png",
        "keywords": "A Path,orange",
        "name": "Apath",
        "type": "staff",
    }
