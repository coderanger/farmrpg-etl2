from typing import Any, Iterable

from lxml.html import html5parser

from utils.parsers import CSSSelector, sel_first_or_die

TR_SEL = CSSSelector("html|tr:not(html|tr:first-of-type)")
TD_ID_SEL = CSSSelector("html|td:nth-of-type(1)")
TD_NAME_SEL = CSSSelector("html|td:nth-of-type(2)")
TD_IMAGE_SEL = CSSSelector("html|td:nth-of-type(3) html|img")
TD_LIKES_SEL = CSSSelector("html|td:nth-of-type(10)")
TD_LOVES_SEL = CSSSelector("html|td:nth-of-type(11)")
TD_HATES_SEL = CSSSelector("html|td:nth-of-type(12)")


def parse_manage_npc(page: bytes) -> Iterable[dict[str, Any]]:
    root = html5parser.document_fromstring(page.decode())
    for row in TR_SEL(root):
        id_elm = sel_first_or_die(TD_ID_SEL(row), "Unable to parse ID from row")
        name_elm = sel_first_or_die(TD_NAME_SEL(row), "Unable to parse name from row")
        image_elm = sel_first_or_die(
            TD_IMAGE_SEL(row), "Unable to parse image from row"
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
