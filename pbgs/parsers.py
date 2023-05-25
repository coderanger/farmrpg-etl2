import re
from typing import Iterable

import attrs

from utils.parsers import CSSSelector, parse_page_fragment, sel_first_or_die


ROW_SEL = CSSSelector("div.col-50")
IMG_SEL = CSSSelector("img")
STRONG_SEL = CSSSelector("strong")
BUTTON_SEL = CSSSelector("button")
COST_RE = re.compile(r"\((?:[0-9,]+/([0-9,]+)|([0-9,]+)x?) ([^)]+)\)")


@attrs.define
class ParsedBackground:
    id: int | None
    name: str
    image: str
    cost_item: str | None
    cost_quantity: int | None


def parse_gallery(page: bytes) -> Iterable[ParsedBackground]:
    root = parse_page_fragment(page)
    for row in ROW_SEL(root):
        button = sel_first_or_die(BUTTON_SEL(row), "Unable to find button")
        if "btnpurple" in button.get("class") or button.get("data-type") == "theme":
            continue
        name = sel_first_or_die(STRONG_SEL(row), "Unable to find title")
        img = sel_first_or_die(IMG_SEL(row), "Unable to find image")
        cost_md = COST_RE.search(button.text)
        raw_id = button.get("data-id")

        yield ParsedBackground(
            id=None if raw_id is None else int(raw_id),
            name=name.text.strip(),
            image=img.get("src"),
            cost_item=None if cost_md is None else cost_md[3],
            cost_quantity=None
            if cost_md is None
            else int((cost_md[1] or cost_md[2]).replace(",", "")),
        )
