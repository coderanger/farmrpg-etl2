import datetime
import re
from typing import Iterable

import attrs
import dateutil.parser

from utils.parsers import (
    CSSSelector,
    parse_page_fragment,
    parse_section,
    sel_first_or_die,
)


COL_SEL = CSSSelector("div.col-50")
LINK_SEL = CSSSelector("a")
PROGRESS_SEL = CSSSelector("div.row ~ strong")
ROW_SEL = CSSSelector("div.item-content")
TITLE_SEL = CSSSelector("div.item-title")
PAST_LINK_SEL = CSSSelector("div.item-media a")
ID_RE = re.compile(r"\?id=(\d+)")
QUANTITY_RE = re.compile(r"(\S[^(]+) \(x?([0-9,]+)\)")
GOAL_QUANTITY_RE = re.compile(r"Goal: (\S[^(]+) \(x?([0-9,]+)\)")
REWARD_QUANTITY_RE = re.compile(r"Reward: (\S[^(]+) \(x?([0-9,]+)\)")
PROGRESS_RE = re.compile(r"([0-9,]+) / (?:[0-9,]+)")


@attrs.define
class ParsedCommunityCenter:
    date: datetime.date | None
    input_item: int | None
    input_item_name: str
    input_quantity: int
    output_item: int
    output_quantity: int
    progress: int


def parse_community_center(
    page: bytes, today: datetime.date
) -> Iterable[ParsedCommunityCenter]:
    root = parse_page_fragment(page)

    # First the current day.
    today_elm = parse_section(root, "Current Goal")
    assert today_elm is not None
    goal_col, reward_col = list(COL_SEL(today_elm))

    goal_link = sel_first_or_die(LINK_SEL(goal_col), "Unable to find goal link")
    goal_link_md = ID_RE.search(goal_link.get("href"))
    assert goal_link_md is not None
    goal_quantity_md = QUANTITY_RE.search(goal_link.getnext().tail)
    assert goal_quantity_md is not None

    reward_link = sel_first_or_die(LINK_SEL(reward_col), "Unable to find reward link")
    reward_link_md = ID_RE.search(reward_link.get("href"))
    assert reward_link_md is not None
    reward_quantity_md = QUANTITY_RE.search(reward_link.getnext().tail)
    assert reward_quantity_md is not None

    progress_elm = sel_first_or_die(PROGRESS_SEL(today_elm), "Unable to find progress")
    progress_md = PROGRESS_RE.search(progress_elm.text)
    assert progress_md is not None

    yield ParsedCommunityCenter(
        date=today,
        input_item=int(goal_link_md[1]),
        input_item_name=goal_quantity_md[1],
        input_quantity=int(goal_quantity_md[2].replace(",", "")),
        output_item=int(reward_link_md[1]),
        output_quantity=int(reward_quantity_md[2].replace(",", "")),
        progress=int(progress_md[1].replace(",", "")),
    )

    # Then the past days.
    last_week = parse_section(root, "Last 7 Days")
    assert last_week is not None
    for row in ROW_SEL(last_week):
        title = sel_first_or_die(TITLE_SEL(row), "Unable to find title")
        date = dateutil.parser.parse(title.text).date()

        link = sel_first_or_die(PAST_LINK_SEL(row), "Unable to find past link")
        link_md = ID_RE.search(link.get("href"))
        assert link_md is not None

        text = "\n".join(row.itertext())
        progress_md = PROGRESS_RE.search(text)
        assert progress_md is not None
        goal_quantity_md = GOAL_QUANTITY_RE.search(text)
        assert goal_quantity_md is not None
        reward_quantity_md = REWARD_QUANTITY_RE.search(text)
        assert reward_quantity_md is not None

        yield ParsedCommunityCenter(
            date=date,
            input_item=None,
            input_item_name=goal_quantity_md[1],
            input_quantity=int(goal_quantity_md[2].replace(",", "")),
            output_item=int(link_md[1]),
            output_quantity=int(reward_quantity_md[2].replace(",", "")),
            progress=int(progress_md[1].replace(",", "")),
        )
