import re
from typing import Iterable

import attrs
from lxml.etree import _Element
from lxml.html import html5parser

from ..utils.parsers import (
    CSSSelector,
    de_namespace,
    parse_page_fragment,
    sel_first_or_die,
)

ROW_SEL = CSSSelector("div.row")
LINK_SEL = CSSSelector("div.col-50 a")
LINK_RE = re.compile(r"^item\.php\?id=(\d+)$")
QUANTITY_RE = re.compile(r"\(x([0-9,]+)\)")
ONESHOT_RE = re.compile(r"This offer can only ever be accepted once")

TR_SEL = CSSSelector("table:first-of-type tr:not(tr:first-of-type)")
TD_ID_SEL = CSSSelector("td:nth-of-type(1)")
TD_CARDS_SEL = CSSSelector("td:nth-of-type(2) img")
TD_REWARD_SEL = CSSSelector("td:nth-of-type(3) img")
ITEM_RE = re.compile(r"(\S[^(]*) \(x([0-9,]+)\)")


@attrs.define
class ParsedTrade:
    input_item: int
    input_quantity: int
    output_item: int
    output_quantity: int
    oneshot: bool


@attrs.define
class ParsedCardTrade:
    id: int
    spades_quantity: int | None
    hearts_quantity: int | None
    diamonds_quantity: int | None
    clubs_quantity: int | None
    joker_quantity: int | None
    output_item: str
    output_quantity: int


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
    root = parse_page_fragment(page)
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


def _parse_card_item(elm: _Element) -> tuple[str, int]:
    md = ITEM_RE.search(elm.tail)
    if md is None:
        raise ValueError(f"Unable to parse item: {elm.tail=}")
    return md[1].strip(), int(md[2].replace(",", ""))


def parse_cards(page: bytes) -> Iterable[ParsedCardTrade]:
    root = de_namespace(html5parser.document_fromstring(page.decode()))
    for row in TR_SEL(root):
        id_elm = sel_first_or_die(TD_ID_SEL(row), "Unable to find ID")
        trade_id = int(id_elm.text)
        inputs = dict(_parse_card_item(card_elm) for card_elm in TD_CARDS_SEL(row))
        assert inputs, "No inputs found"
        output_elm = sel_first_or_die(TD_REWARD_SEL(row), "Unable to find reward")
        output_item, output_quantity = _parse_card_item(output_elm)

        spades_quantity = inputs.pop("Spades", None)
        hearts_quantity = inputs.pop("Hearts", None)
        diamonds_quantity = inputs.pop("Diamonds", None)
        clubs_quantity = inputs.pop("Clubs", None)
        joker_quantity = inputs.pop("Joker", None)
        assert not inputs, f"Extra inputs found: {inputs=}"

        yield ParsedCardTrade(
            id=trade_id,
            spades_quantity=spades_quantity,
            hearts_quantity=hearts_quantity,
            diamonds_quantity=diamonds_quantity,
            clubs_quantity=clubs_quantity,
            joker_quantity=joker_quantity,
            output_item=output_item,
            output_quantity=output_quantity,
        )
