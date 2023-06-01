import datetime
import re
import urllib.parse
from typing import Any, Iterable

import attrs
import dateutil.parser
from lxml.html import tostring

from utils.parsers import (
    CSSSelector,
    parse_page_fragment,
    sel_first_or_die,
)

UPDATES_SEL = CSSSelector("div.recentUpdates")
DATE_SEL = CSSSelector("div.card-header a")
CONTENT_SEL = CSSSelector("div.card-content-inner")
ID_RE = re.compile(r"\?id=(\d+)")
GAME_PAGE_RE = re.compile(r"^[a-zA-Z0-9_-]+\.php(\?.*)?(#.*)?$")
NEWLINES_RE = re.compile("\n{2,}")
FORCEPATH_RE = re.compile(r"<strong>\w+path</strong>")
TENFOO_RE = re.compile(r"<strong>\w+foo</strong>")


@attrs.define
class ParsedUpdate:
    id: int
    date: datetime.date
    content: str
    clean_content: str
    text_content: str


def parse_updates(page: bytes) -> Iterable[dict[str, Any]]:
    root = parse_page_fragment(page)
    for elm in UPDATES_SEL(root):
        date_elm = sel_first_or_die(DATE_SEL(elm), "Unable to parse date from update")
        content_elm = sel_first_or_die(
            CONTENT_SEL(elm), "Unable to parse content from update"
        )

        id_md = ID_RE.search(date_elm.get("href"))
        if id_md is None:
            raise ValueError("Unable to parse ID")
        update_id = int(id_md[1])
        date = dateutil.parser.parse("".join(date_elm.itertext())).date()
        inner_content = "".join(tostring(e, encoding="unicode") for e in content_elm)
        content = f"{content_elm.text}{inner_content}"
        # Fix the change-every-time-they-render macros
        content = FORCEPATH_RE.sub("<strong>Forcepath</strong>", content)
        content = TENFOO_RE.sub("<strong>Tenfoo</strong>", content)
        item_names = set()

        # Generate a version of the content that has no relative links.
        for elm in content_elm.iterdescendants("a"):
            href = elm.get("href")
            if GAME_PAGE_RE.match(href):
                href = f"index.php#!/{href}"
            elm.attrib["href"] = urllib.parse.urljoin("https://farmrpg.com/", href)
        for elm in content_elm.iterdescendants("img"):
            elm.attrib["src"] = urllib.parse.urljoin(
                "https://farmrpg.com/", elm.get("src")
            )
            if "itemimgsm" in elm.get("class", ""):
                if elm.get("alt"):
                    item_names.add(elm.get("alt"))
                elm.attrib["style"] = f"{elm.get('style', '')};width:25px;height:25px"
                elm.attrib["width"] = "25"
                elm.attrib["height"] = "25"
        for elm in content_elm.iterdescendants():
            if "class" in elm.attrib:
                del elm.attrib["class"]
        inner_clean_content = "".join(
            tostring(e, encoding="unicode") for e in content_elm
        )
        clean_content = f"{content_elm.text}{inner_clean_content}"

        # Generate just the text content.
        for elm in content_elm.iterdescendants("br"):
            if not elm.tail or not elm.tail.startswith("\n"):
                elm.tail = f"\n{elm.tail or ''}"
        for elm in content_elm.iterdescendants("img"):
            parent = elm.getparent()
            sib = parent.getnext()
            if (
                parent.tag == "a"
                and sib.tag == "span"
                and sib.get("style") == "display:none"
                and sib.text.strip() == elm.get("alt").strip()
            ):
                continue
            if not elm.text and elm.get("alt"):
                elm.text = elm.get("alt")
        text_content = NEWLINES_RE.sub("\n\n", "".join(content_elm.itertext())).strip()
        for item_name in item_names:
            escaped_name = re.escape(item_name)
            text_content = re.sub(
                f"({escaped_name}|\({escaped_name}\)) ({escaped_name}|\({escaped_name}\))",
                item_name,
                text_content,
            )

        yield ParsedUpdate(
            id=update_id,
            date=date,
            content=content,
            clean_content=clean_content,
            text_content=text_content,
        )
