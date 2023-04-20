import structlog
from asgiref.sync import sync_to_async

from utils.http import client
from utils.tasks import AsyncPool

from .models import User
from .parsers import parse_online, parse_profile
from .serializers import UserSerializer

log = structlog.stdlib.get_logger(mod="users.tasks")


CONCURRENT_SCRAPES = 25


NPCS = {
    "Beatrix",
    "Rosalie",
    "Holger",
    "Thomas",
    "Cecil",
    "George",
    "Jill",
    "Vincent",
    "Lorn",
    "Buddy",
    "Borgen",
    "Ric Ryph",
    "Mummy",
    "Star Meerif",
    "Charles Horsington III",
    "ROOMBA",
    "Captain Thomas",
    "frank",
    "Mariya",
}


async def scrape_profile(username: str):
    log.debug("Scraping user", username=username)
    resp = await client.get("/profile.php", params={"user_name": username})
    resp.raise_for_status()
    data = parse_profile(username, resp.content)
    user = await User.objects.filter(id=data["id"]).afirst()
    ser = UserSerializer(instance=user, data=data)
    await sync_to_async(lambda: ser.is_valid(raise_exception=True))()
    await sync_to_async(ser.save)()


async def scrape_from_userlist(url: str, params: dict[str, str] = {}):
    resp = await client.get(url, params=params)
    resp.raise_for_status()
    pool = AsyncPool(CONCURRENT_SCRAPES)
    for username in parse_online(resp.content):
        if username in NPCS:
            continue
        pool.add(scrape_profile(username), name=f"scrape-user-{username}")
    await pool.wait()


async def scrape_all_from_online():
    log.info("Scraping all users from online list")
    await scrape_from_userlist("online.php")


async def scrape_all_from_stafflist():
    log.info("Scraping all users from staff list")
    await scrape_from_userlist("members.php", params={"type": "staff"})
