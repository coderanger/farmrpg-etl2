import re
from typing import Any, Iterable
from urllib.parse import parse_qs, urlsplit

from utils.parsers import CSSSelector, parse_page_fragment, sel_first_or_die

NAME_SEL = CSSSelector(".center.sliding")
IMAGE_SEL = CSSSelector(".exploreimg")
ITEM_SEL = CSSSelector("html|a > html|img.itemimg")
ITEM_ID_RE = re.compile(r"^item\.php\?id=(\d+)$")
LOCATION_SEL = CSSSelector("html|a.item-link")


def parse_location(page: bytes) -> dict[str, Any]:
    root = parse_page_fragment(page)
    name_elm = sel_first_or_die(NAME_SEL(root), "Unable to find name element")
    image_elm = sel_first_or_die(IMAGE_SEL(root), "Unable to find image element")
    items = []
    for elm in ITEM_SEL(root):
        link_elm = elm.getparent()
        assert link_elm is not None
        md = ITEM_ID_RE.match(link_elm.attrib["href"])
        if md is not None:
            items.append(int(md[1]))
    return {
        "name": name_elm.text.strip(),
        "image": image_elm.attrib["src"],
        "items": items,
    }


def parse_locations(page: bytes) -> Iterable[tuple[str, int]]:
    root = parse_page_fragment(page)
    for elm in LOCATION_SEL(root):
        uri = urlsplit(elm.attrib["href"])
        assert uri.path == "location.php"
        params = parse_qs(uri.query)
        yield params["type"][0], int(params["id"][0])
