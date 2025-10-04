from typing import Any, Iterable

from lxml.html import html5parser

from ..utils.parsers import (
    CSSSelector,
    de_namespace,
    parse_page_fragment,
    sel_first_or_die,
)

TR_SEL = CSSSelector("tr:not(tr:first-of-type)")
TD_ID_SEL = CSSSelector("td:nth-of-type(1)")
TD_NAME_SEL = CSSSelector("td:nth-of-type(2)")
TD_IMAGE_SEL = CSSSelector("td:nth-of-type(3) img")
TD_CAN_SEND_SEL = CSSSelector("td:nth-of-type(10)")
TD_LIKES_SEL = CSSSelector("td:nth-of-type(11)")
TD_LOVES_SEL = CSSSelector("td:nth-of-type(12)")
TD_HATES_SEL = CSSSelector("td:nth-of-type(13)")
A_MAILBOX_SEL = CSSSelector("a[href^='mailbox.php?id=']")


def parse_manage_npc(page: bytes) -> Iterable[dict[str, Any]]:
    root = de_namespace(html5parser.document_fromstring(page.decode()))
    for row in TR_SEL(root):
        id_elm = sel_first_or_die(TD_ID_SEL(row), "Unable to parse ID from row")
        name_elm = sel_first_or_die(TD_NAME_SEL(row), "Unable to parse name from row")
        image_elm = sel_first_or_die(
            TD_IMAGE_SEL(row), "Unable to parse image from row"
        )
        can_send_elm = sel_first_or_die(
            TD_CAN_SEND_SEL(row), "Unable to parse can_send from row"
        )
        likes_elm = sel_first_or_die(
            TD_LIKES_SEL(row), "Unable to parse likes from row"
        )
        loves_elm = sel_first_or_die(
            TD_LOVES_SEL(row), "Unable to parse loves from row"
        )
        hates_elm = sel_first_or_die(
            TD_HATES_SEL(row), "Unable to parse hates from row"
        )

        yield {
            "id": int(id_elm.text.strip()),
            "name": name_elm.text.strip(),
            "image": image_elm.attrib["src"],
            "can_send": [
                val.strip() for val in (can_send_elm.text or "").split(",") if val.strip()
            ],
            "likes": [
                val.strip() for val in (likes_elm.text or "").split(",") if val.strip()
            ],
            "loves": [
                val.strip() for val in (loves_elm.text or "").split(",") if val.strip()
            ],
            "hates": [
                val.strip() for val in (hates_elm.text or "").split(",") if val.strip()
            ],
        }


def parse_npclevels(page: bytes) -> Iterable[int]:
    root = parse_page_fragment(page)
    for elm in A_MAILBOX_SEL(root):
        yield int(elm.get("href")[15:])
