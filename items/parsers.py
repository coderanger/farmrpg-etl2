import re
from typing import Iterable

import attrs
from lxml.etree import _Element

from utils.parsers import (
    de_namespace,
    parse_page_fragment,
    parse_section,
    CSSSelector,
    sel_first_or_die,
)

ITEM_SEL = CSSSelector("a.item-link")
TITLE_SEL = CSSSelector("div.item-title strong")
AFTER_SEL = CSSSelector("div.item-after")
ITEM_LINK_RE = re.compile(r"^item\.php\?id=(\d+)$")
AFTER_RE = re.compile(r"(\d+)x")


@attrs.define
class ParsedIngredient:
    id: int
    quantity: int
    gold: bool = False


@attrs.define
class ParsedItem:
    recipe: list[ParsedIngredient]
    locksmith: list[ParsedIngredient]


def _parse_item_section(elm: _Element | None) -> Iterable[ParsedIngredient]:
    if elm is None:
        return

    for item_elm in ITEM_SEL(elm.getnext()):
        title_elm = sel_first_or_die(TITLE_SEL(item_elm), "Unable to find title")
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
    root = de_namespace(parse_page_fragment(content))
    crafting_recipe = list(_parse_item_section(parse_section(root, "Crafting Recipe")))
    cooking_recipe = list(_parse_item_section(parse_section(root, "Cooking Recipe")))
    assert not (
        crafting_recipe and cooking_recipe
    ), "Both crafting and cooking recipes set"
    return ParsedItem(
        recipe=crafting_recipe or cooking_recipe,
        locksmith=list(_parse_item_section(parse_section(root, "Item Contents"))),
    )
