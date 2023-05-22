import re
from typing import Callable, Iterable

from lxml import cssselect, etree
from lxml.etree import QName, _Comment, _Element, _ProcessingInstruction
from lxml.html import html5parser

Selector = Callable[[_Element], list[_Element]]


def CSSSelector(selector: str) -> Selector:
    return cssselect.CSSSelector(
        selector, namespaces={"html": "http://www.w3.org/1999/xhtml"}, translator="html"
    )


SECTION_TITLE_SEL = CSSSelector(".content-block-title")


class ParseError(Exception):
    pass


def parse_page_fragment(page: bytes) -> _Element:
    root = html5parser.fragment_fromstring(page.decode(), create_parent=True)
    return de_namespace(root)


def de_namespace(root: _Element) -> _Element:
    """LXML really cares about XML namespaces and I really don't."""
    for elem in root.getiterator():
        # Skip comments and processing instructions,
        # because they do not have names
        if not (isinstance(elem, _Comment) or isinstance(elem, _ProcessingInstruction)):
            # Remove a namespace URI in the element's name
            elem.tag = QName(elem).localname
    etree.cleanup_namespaces(root)
    return root


def sel_first(elms: list[_Element]) -> _Element | None:
    return next(iter(elms), None)


def sel_first_or_die(elms: list[_Element], error: str) -> _Element:
    elm = sel_first(elms)
    if elm is None:
        raise ParseError(error)
    return elm


def parse_all_sections(root: _Element) -> Iterable[tuple[str, _Element]]:
    for elm in SECTION_TITLE_SEL(root):
        yield elm.text.strip(), elm.getnext()


def _test_regex(title: re.Pattern, val: str) -> bool:
    return title.search(val) is not None


def _test_str(title: str, val: str) -> bool:
    return title == val


def parse_section(root: _Element, title: str | re.Pattern) -> _Element | None:
    test = _test_regex if isinstance(title, re.Pattern) else _test_str
    for section_title, section in parse_all_sections(root):
        if test(title, section_title):
            return section
    return None
