import os

import httpx


def _client(cookie: str) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url="https://farmrpg.com/",
        cookies={"HighwindFRPG": cookie},
        headers={
            "Referer": "https://farmrpg.com/",
            "User-Agent": "farmrpg-etl2 (contact coderanger)",
        },
    )


client = _client(os.environ.get("AUTH_COOKIE", ""))
bot_client = _client(os.environ.get("BOT_AUTH_COOKIE", ""))
