from typing import Any, Iterable

from utils.parsers import CSSSelector, parse_page_fragment, sel_first_or_die


def parse_password_log(page: bytes) -> Iterable[dict[str, Any]]:
    raise NotImplementedError
