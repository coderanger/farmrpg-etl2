import re
from typing import Iterable

import attrs
from lxml.etree import _Element

from utils.parsers import CSSSelector, parse_page_fragment, de_namespace

ROW_SEL = CSSSelector("div.row")
LINK_SEL = CSSSelector("div.col-50 a")
LINK_RE = re.compile(r"^item\.php\?id=(\d+)$")
QUANTITY_RE = re.compile(r"\(x([0-9,]+)\)")
ONESHOT_RE = re.compile(r"This offer can only ever be accepted once")


@attrs.define
class ParsedTrade:
    input_item: int
    input_quantity: int
    output_item: int
    output_quantity: int
    oneshot: bool


def _parse_link(link_elm: _Element) -> tuple[int, int]:
    link_md = LINK_RE.match(link_elm.get("href"))
    if link_md is None:
        raise ValueError("Unable to parse link")
    quantity_text = link_elm.getnext().tail
    quantity_md = QUANTITY_RE.search(quantity_text)
    if quantity_md is None:
        raise ValueError(f"Unable to parse quantity: {quantity_text=}")
    return int(link_md[1]), int(quantity_md[1].replace(",", ""))


def parse_exchange_center(page: bytes) -> Iterable[ParsedTrade]:
    root = de_namespace(parse_page_fragment(page))
    for row in ROW_SEL(root):
        input_link, output_link = list(LINK_SEL(row))
        input_item, input_quantity = _parse_link(input_link)
        output_item, output_quantity = _parse_link(output_link)
        oneshot_elm = row.getnext()
        oneshot = bool(oneshot_elm.text and ONESHOT_RE.search(oneshot_elm.text))
        yield ParsedTrade(
            input_item=input_item,
            input_quantity=input_quantity,
            output_item=output_item,
            output_quantity=output_quantity,
            oneshot=oneshot,
        )
