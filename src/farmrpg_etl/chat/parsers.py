import re
from datetime import datetime, timedelta
from typing import Any, Iterable, cast
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, Tag

from ..utils.parsers import CSSSelector, ParseError

UTC = ZoneInfo("UTC")
SERVER_TIME = ZoneInfo("America/Chicago")

MESSAGE_ID_RE = re.compile(r"^javascript:(?:un)?delChat\((\d+)\)$")
FLAGS_RE = re.compile(r"^(\d+) flags?$")
FORCEPATH_RE = re.compile(r"<strong>\w+path</strong>")
TENFOO_RE = re.compile(r"<strong>\w+foo</strong>")
FIRESTREAM_RE = re.compile(r"<strong>\w+stream</strong>")
CODERANGER_RE = re.compile(r"<strong>code\w+</strong>")
AT_LINK_RE = re.compile(
    r'<a class="close-panel" href="profile.php\?user_name=[^">]+"'
    r' style="color:teal">(@[^">]+)</a>'
)
EMBLEM_SEL = CSSSelector("a.setemblembtn > img.vendoritemimg")
EMBLEM_NAME_RE = re.compile(r"(96)?(test)?$")
EMBLEM_NAME_RE2 = re.compile(r"[_.-]+")
EMBLEM_NAME_RE3 = re.compile(r"([a-z])([A-Z0-9])")
EMBLEM_UUID_RE = re.compile(
    r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
)


def parse_chat(content: bytes) -> Iterable[dict[str, Any]]:
    """Parse the chat HTML."""
    # This has a bunch of ugly casts because the type stubs for BS aren't great.
    # (or rather the interface isn't built for strong typing, sigh)
    root = BeautifulSoup(content, "lxml")
    last_ts = datetime.now(tz=SERVER_TIME)
    for elm in root.select("div.chat-txt"):
        # Parse out the timestamp, which is weirdly difficult.
        ts_elm = elm.select_one("span")
        if ts_elm is None:
            raise ParseError(f"Unable to find timestamp: {content.decode()}")
        ts = datetime.strptime(ts_elm.text.strip(), "%I:%M:%S %p").replace(
            year=last_ts.year,
            month=last_ts.month,
            day=last_ts.day,
            tzinfo=last_ts.tzinfo,
        )
        if ts > last_ts:
            # Day rollover, this was actually yesterday.
            ts = ts - timedelta(days=1)
        last_ts = ts
        # Find the chat message ID.
        chip_elm = elm.select_one("div.chip")
        if chip_elm is None:
            raise ParseError(f"Unable to find chip: {content.decode()}")
        message_id_a_elm = cast(Tag | None, chip_elm.find_next_sibling("a"))
        if message_id_a_elm is None:
            raise ParseError(f"Unable to find message ID link: {content.decode()}")
        message_id_match = MESSAGE_ID_RE.match(cast(str, message_id_a_elm["href"]))
        if message_id_match is None:
            raise ParseError(f"Unable to parse message ID: {message_id_a_elm['href']}")
        # Then the rest of the stuff is easy.
        emblem_elm = elm.select_one("div.chip-media img")
        if emblem_elm is None:
            raise ParseError(f"Unable to find emblem: {content.decode()}")
        icons_elm = elm.select_one("i.f7-icons")
        if icons_elm is None:
            raise ParseError(f"Unable to find icons: {content.decode()}")
        content_elm = cast(Tag | None, icons_elm.find_next("span"))
        if content_elm is None:
            raise ParseError(f"Unable to find content span: {content.decode()}")
        msg_content = content_elm.decode_contents(formatter="html5")
        msg_content = FORCEPATH_RE.sub("<strong>Forcepath</strong>", msg_content)
        msg_content = TENFOO_RE.sub("<strong>Tenfoo</strong>", msg_content)
        msg_content = FIRESTREAM_RE.sub("<strong>Firestream</strong>", msg_content)
        msg_content = CODERANGER_RE.sub("<strong>coderanger</strong>", msg_content)
        msg_content = AT_LINK_RE.sub(r"\1:", msg_content)
        yield {
            "id": int(message_id_match[1]),
            "ts": ts.astimezone(UTC),
            "emblem": cast(str, emblem_elm["src"]).rsplit("/", 1)[-1],
            "username": cast(str, emblem_elm["data-username"]),
            "content": msg_content,
            "deleted": "redstripes" in elm["class"],
        }


def parse_flags(content: bytes) -> Iterable[dict[str, Any]]:
    """Parse the flag log HTML."""
    # This has a bunch of ugly casts because the type stubs for BS aren't great.
    # (or rather the interface isn't built for strong typing, sigh)
    root = BeautifulSoup(content, "lxml")
    now = datetime.now(tz=SERVER_TIME)
    for elm in root.select("li"):
        title_elm = elm.select_one(".item-title")
        if title_elm is None:
            raise ParseError(f"Unable to find item title: {content.decode()}")
        after_elm = elm.select_one(".item-after")
        if after_elm is None:
            raise ParseError(f"Unable to find item after: {content.decode()}")
        parts = list(title_elm.stripped_strings)
        ts = datetime.strptime(parts[0], "%b %d, %I:%M:%S %p").replace(
            year=now.year, tzinfo=SERVER_TIME
        )
        if ts > now:
            # Year rollover, this was actually last year.
            ts.replace(year=ts.year - 1)
        flags_match = FLAGS_RE.match(after_elm.string or "")
        yield {
            "id": int(elm["data-id"]),
            "ts": ts.astimezone(UTC),
            "emblem": "",
            "username": parts[1],
            "content": parts[2][2:],
            "deleted": elm["data-deleted"] == "1",
            "flags": int(flags_match[1]) if flags_match else 0,
        }
