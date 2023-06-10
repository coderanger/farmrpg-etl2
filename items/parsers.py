import re
from typing import Iterable

import attrs
from lxml.etree import _Element

from utils.parsers import (
    parse_page_fragment,
    parse_section,
    CSSSelector,
    sel_first_or_die,
)

ITEM_SEL = CSSSelector("a.item-link")
TITLE_SEL = CSSSelector("div.item-title")
TITLE_STRONG_SEL = CSSSelector("div.item-title strong")
AFTER_SEL = CSSSelector("div.item-after")
ITEM_LINK_RE = re.compile(r"^item\.php\?id=(\d+)$")
AFTER_RE = re.compile(r"(\d+)x")
FLEA_MARKET_RE = re.compile(r"([0-9,]+) Gold")


@attrs.define
class ParsedIngredient:
    id: int
    quantity: int
    gold: bool = False


@attrs.define
class ParsedItem:
    recipe: list[ParsedIngredient]
    locksmith: list[ParsedIngredient]
    flea_market_price: int | None
    from_event: bool


def _parse_recipe(elm: _Element | None) -> Iterable[ParsedIngredient]:
    if elm is None:
        return

    for item_elm in ITEM_SEL(elm.getnext()):
        title_elm = sel_first_or_die(TITLE_STRONG_SEL(item_elm), "Unable to find title")
        after_elm = sel_first_or_die(AFTER_SEL(item_elm), "Unable to find item-after")

        if title_elm.text.strip() == "Gold":
            yield ParsedIngredient(
                id=0,
                gold=True,
                # Gold doesn't have the trailing x.
                quantity=int(after_elm.text.strip()),
            )
            continue

        after_md = AFTER_RE.match(after_elm.text or "")
        if after_md is None:
            raise ValueError("Unable to parse item-after")
        link_md = ITEM_LINK_RE.match(item_elm.get("href", ""))
        if link_md is None:
            raise ValueError("Unable to parse item link")
        yield ParsedIngredient(
            id=int(link_md.group(1)),
            quantity=int(after_md.group(1)),
        )


def parse_item(content: bytes) -> ParsedItem:
    root = parse_page_fragment(content)
    crafting_recipe = list(_parse_recipe(parse_section(root, "Crafting Recipe")))
    cooking_recipe = list(_parse_recipe(parse_section(root, "Cooking Recipe")))
    assert not (
        crafting_recipe and cooking_recipe
    ), "Both crafting and cooking recipes set"

    flea_market_price = None
    from_event = False
    details = parse_section(root, "Item Details")
    assert details is not None
    for elm in TITLE_SEL(details):
        name = elm.text.strip()
        if name == "Flea Market":
            after_elm = sel_first_or_die(
                AFTER_SEL(elm.getparent()), "Unable to find item-after"
            )
            after_md = FLEA_MARKET_RE.search(after_elm.text)
            assert after_md is not None
            flea_market_price = int(after_md[1].replace(",", ""))
        elif name == "Event Item":
            after_elm = sel_first_or_die(
                AFTER_SEL(elm.getparent()), "Unable to find item-after"
            )
            if "Yes" in after_elm.text:
                from_event = True

    return ParsedItem(
        recipe=crafting_recipe or cooking_recipe,
        locksmith=list(_parse_recipe(parse_section(root, "Item Contents"))),
        flea_market_price=flea_market_price,
        from_event=from_event,
    )
