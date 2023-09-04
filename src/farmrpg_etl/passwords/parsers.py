import re
from typing import Iterable

import attrs

from ..utils.parsers import CSSSelector, parse_page_fragment, sel_first_or_die

ROW_SEL = CSSSelector("li.item-content")
TITLE_SEL = CSSSelector("div.item-title span:first-of-type")
IMG_SEL = CSSSelector("div.item-after img")
REWARD_RE = re.compile(r"(\S.*?) \(x?([0-9,]+)\)")


@attrs.define
class ParsedPassword:
    password: str
    rewards: dict[str, int] = attrs.Factory(dict)


def parse_password_log(page: bytes) -> Iterable[ParsedPassword]:
    root = parse_page_fragment(page)
    for row in ROW_SEL(root):
        title = sel_first_or_die(TITLE_SEL(row), "Unable to find title")
        parsed = ParsedPassword(password=title.text.strip().lower())
        for img in IMG_SEL(row):
            md = REWARD_RE.search(img.tail)
            if md is None:
                raise ValueError(f"Unable to parse reward from {img.tail=}")
            parsed.rewards[md[1].strip()] = int(md[2].replace(",", ""))
        yield parsed
