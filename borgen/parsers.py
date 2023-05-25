import re
from typing import Iterable

import attrs

from utils.parsers import (
    CSSSelector,
    parse_page_fragment,
    sel_first,
    sel_first_or_die,
    parse_section,
)

ROW_SEL = CSSSelector("div.item-content")
LINK_SEL = CSSSelector("div.item-media a")
PRICE_SEL = CSSSelector("div.item-after button")
PRICE2_SEL = CSSSelector("div.item-after button.buybtn span")
ID_RE = re.compile(r"\?id=(\d+)")
PRICE_RE = re.compile(r"([0-9,]+) AC")


@attrs.define
class ParsedItem:
    item: int
    price: int | None


def parse_borgens(page: bytes) -> Iterable[ParsedItem]:
    root = parse_page_fragment(page)
    items = parse_section(root, "Take a look")
    assert items is not None
    for row in ROW_SEL(items):
        link_elm = sel_first_or_die(LINK_SEL(row), "Unable to find link")
        link_md = ID_RE.search(link_elm.get("href"))
        assert link_md is not None
        price_elm = sel_first(PRICE_SEL(row))
        price = None
        if price_elm is not None and price_elm.text is not None:
            price_md = PRICE_RE.search(price_elm.text)
            if price_md is not None:
                price = int(price_md[1].replace(",", ""))
        else:
            price_elm = sel_first(PRICE2_SEL(row))
            if price_elm is not None and price_elm.text is not None:
                price = int(price_elm.text.replace(",", ""))
        yield ParsedItem(
            item=int(link_md[1]),
            price=price,
        )
