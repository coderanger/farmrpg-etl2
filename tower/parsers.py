import re
from typing import Iterable

import attrs


LEVEL_RE = re.compile(
    r"""Level(?:\n|\r\n)
(\d+)(?:\n|\r\n)
You\ got:(?:\n|\r\n)
([^(\n]+)\ \(x([0-9,]+)\)(?:\n|\r\n)
([^(\n]+)\ \(x([0-9,]+)\)(?:\n|\r\n)
([^(\n]+)\ \(x([0-9,]+)\)""",
    re.MULTILINE | re.VERBOSE,
)


@attrs.define
class ParsedTowerReward:
    level: int
    order: int
    item: str
    quantity: int


def parse_tower_txt(text: str) -> Iterable[ParsedTowerReward]:
    for md in LEVEL_RE.finditer(text):
        level = int(md[1])
        yield ParsedTowerReward(
            level=level,
            order=1,
            item=md[2],
            quantity=int(md[3].replace(",", "")),
        )
        yield ParsedTowerReward(
            level=level,
            order=2,
            item=md[4],
            quantity=int(md[5].replace(",", "")),
        )
        yield ParsedTowerReward(
            level=level,
            order=3,
            item=md[6],
            quantity=int(md[7].replace(",", "")),
        )
