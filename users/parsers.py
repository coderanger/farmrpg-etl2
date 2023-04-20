import re
import urllib.parse
from typing import Any, Iterable, Literal, cast

import structlog
from bs4 import BeautifulSoup, Tag

from utils.parsers import ParseError

FRIENDS_LINK_RE = re.compile(r"^members.php\?type=friended&id=(\d+)$")
ONLINE_PROFILE_RE = re.compile(r"^profile.php\?")

log = structlog.stdlib.get_logger(mod="users.parsers")


def parse_role(root: BeautifulSoup) -> Literal["farmhand", "ranger", "admin"] | None:
    """Parse profile bagdes to find a role badge."""
    badges_card_elm = root.select_one(".card")
    if badges_card_elm is None:
        return None
    admin_image_elm = badges_card_elm.select_one("img[src='/img/items/admin.png']")
    if admin_image_elm is None:
        return None
    role_stong_elm = cast(Tag | None, admin_image_elm.find_next_sibling("strong"))
    if role_stong_elm is None:
        raise ParseError("No role strong found")
    role = role_stong_elm.text.strip()
    if role == "Farm Hand":
        return "farmhand"
    elif role == "Ranger":
        return "ranger"
    elif role == "Admin":
        return "admin"
    raise ParseError(f"Unknown role string: {role!r}")


def parse_profile(username: str, content: bytes) -> dict[str, Any]:
    root = BeautifulSoup(content, "lxml")
    # Parse user ID from the friends link.
    friends_a_elm = cast(Tag | None, root.find("a", href=FRIENDS_LINK_RE))
    if friends_a_elm is None:
        raise ParseError(f"Unable to find friends link: {content.decode()}")
    friends_href = cast(str, friends_a_elm["href"])
    user_id_match = FRIENDS_LINK_RE.match(friends_href)
    if user_id_match is None:
        # This should be impossible, it's the same regex as used to find it.
        raise ParseError("Friends link regex did not match")
    user_id = int(user_id_match.group(1))
    # Grab the role.
    role = parse_role(root)
    # Build the data.
    return {
        "id": user_id,
        "username": username,  # TODO: This should parse from the profile itself for casing differences.
        "role": role,
    }


def parse_online(content: bytes) -> Iterable[str]:
    root = BeautifulSoup(content, "lxml")
    for elm in root.find_all("a", href=ONLINE_PROFILE_RE):
        href = cast(str, elm["href"])
        qs = urllib.parse.parse_qs(href.split("?", 1)[1])
        yield qs["user_name"][0]
