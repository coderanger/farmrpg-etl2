from pathlib import Path

import pytest

from .parsers import parse_password_log, ParsedPassword

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def popwlog() -> bytes:
    return FIXTURES_ROOT.joinpath("popwlog.html").open("rb").read()


def test_parse_password_log(popwlog: bytes):
    passwords = list(parse_password_log(popwlog))
    assert len(passwords) == 179
    assert passwords[0] == ParsedPassword(
        password="kristoff", rewards={"Christmas Tree": 1}
    )
    assert passwords[20] == ParsedPassword(
        password="signers", rewards={"Red Dye": 5, "White Parchment": 5, "Blue Dye": 5}
    )
    assert passwords[22] == ParsedPassword(
        password="0x8173074", rewards={"Silver": 250_000, "Gold": 10}
    )
