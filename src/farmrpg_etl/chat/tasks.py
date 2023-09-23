import asyncio
import html
import re
import time
from datetime import datetime
from typing import Any
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import httpx
import sentry_sdk
import structlog
from asgiref.sync import sync_to_async
from async_lru import alru_cache
from django.conf import settings
from django.utils import timezone
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import firestore

from ..cron.decorators import cron
from ..users.models import User
from ..utils.http import alpha_client
from ..utils.http import client as prod_client
from ..utils.tasks import AsyncPool
from .models import Emblem, GameEmblem, Message
from .parsers import parse_chat, parse_emblems, parse_flags
from .serailizers import EmblemSerializer, MessageSerializer

log = structlog.stdlib.get_logger(mod="chat.tasks")

# List of chat rooms to process (not including "alpha" because it is special).
ROOMS = ["help", "global", "spoilers", "trade", "giveaways", "trivia", "staff"]

MATTERBRIDGE_GATEWAYS = {
    "staff": "staff2",
    "alpha": "alpha2",
}
MATTERBRIDGE_CLIENT = (
    httpx.AsyncClient(base_url=settings.MATTERBRIDGE_API)
    if settings.MATTERBRIDGE_API is not None
    else None
)
STARTUP_TIME = timezone.now()

# Global cache of previously-seen messages for deleted_ts detection.
# {room: {msg.id: msg_data}}
LAST_MESSAGES: dict[str, dict[int, dict[str, Any]]] = {}
LAST_FLAGS: dict[str, dict[int, int]] = {}

UTC = ZoneInfo("UTC")

MENTION_RE = re.compile(r"@([^:\s]+(?:[^:]{0,29}?[^:\s](?=:))?)")
LINK_RE = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>([^<]*)</a>')
I_RE = re.compile(r"<i[^>]*>([^<]*)</i>")

try:
    db = firestore.AsyncClient(project="farmrpg-mod")
    rooms_col = db.collection("rooms")
except DefaultCredentialsError:
    db = rooms_col = None


def _replace_link(md: re.Match) -> str:
    href: str = md.group(1)
    text: str = md.group(2)
    # Make sure URLs resolve fully.
    if not (
        href.startswith("https://")
        or href.startswith("http://")
        or href.startswith("/")
    ):
        href = f"https://farmrpg.com/index.php#!/{href}"
    elif href.startswith("/"):
        href = urljoin("https://farmrpg.com/", href)
    return f"[{text}]({href})"


async def _matterbridge_send(room: str, msg_data: dict[str, Any]):
    # Fix up links.
    content = I_RE.sub("*\\1*", msg_data["content"])
    content = LINK_RE.sub(_replace_link, content)
    content = html.unescape(content)
    resp = await MATTERBRIDGE_CLIENT.post(
        "/api/message",
        json={
            "text": content,
            "username": msg_data["username"],
            "gateway": MATTERBRIDGE_GATEWAYS[room],
            "avatar": f"https://farmrpg.com/img/emblems/{msg_data['emblem']}",
        },
    )
    log.debug("Matterbridge send", room=room, id=msg_data["id"], resp=resp.status_code)
    resp.raise_for_status()


@alru_cache(maxsize=100)
async def _get_id_for_user(username: str) -> int | None:
    return (
        await User.objects.values_list("id", flat=True)
        .filter(username=username)
        .afirst()
    )


async def scrape_chat(
    room: str,
    client: httpx.AsyncClient = prod_client,
    game_room: str | None = None,
):
    log.debug("Starting chat scrape", room=room)
    resp = await client.get(
        "worker.php",
        params={
            "go": "getchat",
            "room": game_room or room,
            "cachebuster": str(time.time()),
        },
    )
    resp.raise_for_status()

    if resp.content == b"no access":
        raise ValueError(f"Got a no access response from room {room}")

    # Parse the HTML.
    msgs = list(parse_chat(resp.content))
    for msg_data in reversed(msgs):
        last_msg = LAST_MESSAGES.get(room, {}).get(msg_data["id"])
        if last_msg is None or msg_data["deleted"] != last_msg["deleted"]:
            log.debug("Got chat message", room=room, msg=msg_data["id"])
            if (
                last_msg is not None
                and last_msg["deleted"] is False
                and msg_data["deleted"] is True
            ):
                msg_data["deleted_ts"] = datetime.now(tz=UTC)

            # Save the message to the database.
            db_data = {**msg_data}
            db_data["room"] = room
            db_data["user_id"] = await _get_id_for_user(db_data["username"])
            msg = await Message.objects.filter(id=db_data["id"]).afirst()
            ser = MessageSerializer(instance=msg, data=db_data)
            await sync_to_async(lambda: ser.is_valid(raise_exception=True))()
            await sync_to_async(ser.save)()

            # Push the message to Firestore.
            fb_data = {**msg_data}
            fb_data["mentions"] = MENTION_RE.findall(msg_data["content"])
            doc_ref = (
                rooms_col.document(room)
                .collection("chats")
                .document(str(msg_data["id"]))
            )
            await doc_ref.set(fb_data, merge=True)
        if (
            last_msg is None
            and not msg_data["deleted"]
            and MATTERBRIDGE_CLIENT is not None
            and room in MATTERBRIDGE_GATEWAYS
            and msg_data["ts"] > STARTUP_TIME
        ):
            # Don't wait for this to finish.
            asyncio.create_task(_matterbridge_send(room, msg_data))

    LAST_MESSAGES[room] = {msg["id"]: msg for msg in msgs}
    log.debug("Finished chat scrape", room=room)


async def scrape_flags(room: str):
    log.debug("Starting flags scrape", room=room)
    resp = await prod_client.get(
        "worker.php",
        params={
            "type": "chat",
            "room": room,
            "flag": "1",
        },
    )
    resp.raise_for_status()

    # Parse the HTML
    msgs = list(parse_flags(resp.content))
    for msg_data in msgs:
        last_flags = LAST_MESSAGES.get(room, {}).get(msg_data["id"])
        if last_flags is None or msg_data["flags"] != last_flags:
            # Save the message to the database.
            db_data = {**msg_data}
            db_data["room"] = room
            msg = await Message.objects.filter(id=db_data["id"]).afirst()
            ser = MessageSerializer(instance=msg, data=db_data)
            await sync_to_async(ser.is_valid)(raise_exception=True)
            await sync_to_async(ser.save)()

            # Push the message to Firestore.
            fb_data = {**msg_data}
            fb_data["mentions"] = MENTION_RE.findall(msg_data["content"])
            doc_ref = (
                rooms_col.document(room)
                .collection("chats")
                .document(str(msg_data["id"]))
            )
            await doc_ref.set(fb_data, merge=True)

    LAST_FLAGS[room] = {msg["id"]: msg["flags"] for msg in msgs}
    log.debug("Finished flags scrape", room=room)


async def scrape_all_chat():
    pool = AsyncPool()
    for room in ROOMS:
        pool.add(scrape_chat(room), name=f"scrape-chat-{room}")
    pool.add(
        scrape_chat("alpha", client=alpha_client, game_room="global"),
        name="scrape-chat-alpha",
    )
    await pool.wait()


async def scrape_all_flags():
    pool = AsyncPool()
    for room in ROOMS:
        pool.add(scrape_flags(room), name=f"scrape-flags-{room}")
    await pool.wait()


@cron("@hourly")
async def scrape_emblems():
    count_total = 0
    count_created = 0
    async for emb in GameEmblem.objects.all().aiterator():
        if emb.vendor_id == 1:
            continue
        _, created = await Emblem.objects.aupdate_or_create(
            id=emb.id,
            defaults={
                "name": emb.name,
                "image": emb.img,
                "type": {999: Emblem.TYPE_PATREON, 1099: Emblem.TYPE_STAFF}.get(
                    emb.vendor_id
                ),
                "keywords": emb.category,
            },
        )
        count_total += 1
        if created:
            count_created += 1
    return {"total": count_total, "created": count_created}
