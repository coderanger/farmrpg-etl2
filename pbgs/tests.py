from pathlib import Path

import pytest

from .parsers import parse_gallery, ParsedBackground

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def gallery() -> bytes:
    return FIXTURES_ROOT.joinpath("gallery.html").open("rb").read()


def test_parse_gallery(gallery: bytes):
    backgrounds = list(parse_gallery(gallery))
    assert len(backgrounds) == 29
    assert backgrounds[0] == ParsedBackground(
        id=1,
        name="The Farm",
        image="/img/pbgs/light/bg_def.jpg",
        cost_item=None,
        cost_quantity=None,
    )
    assert backgrounds[1] == ParsedBackground(
        id=3,
        name="Buddy's Cave",
        image="/img/pbgs/light/bg_20.jpg",
        cost_item="Model Ship",
        cost_quantity=10,
    )
    assert backgrounds[5] == ParsedBackground(
        id=None,
        name="Money Money Money",
        image="/img/pbgs/light/bg_64.jpg",
        cost_item="Borgen Buck",
        cost_quantity=100,
    )
    assert backgrounds[14] == ParsedBackground(
        id=15,
        name="Stone Road",
        image="/img/pbgs/light/bg_07.jpg",
        cost_item="Gold",
        cost_quantity=100,
    )
    assert backgrounds[22] == ParsedBackground(
        id=12,
        name="Lost Merchant",
        image="/img/pbgs/light/bg_39.jpg",
        cost_item="Silver",
        cost_quantity=1_000_000_000,
    )
