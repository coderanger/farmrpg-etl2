import os

import httpx


def _client(cookie: str, prefix: str = "") -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=f"https://{prefix}farmrpg.com/",
        # base_url="http://localhost:8000/",
        cookies={"HighwindFRPG": cookie},
        headers={
            "Referer": f"https://{prefix}farmrpg.com/",
            "User-Agent": "farmrpg-etl2 (contact coderanger)",
        },
        timeout=10000,
    )


client = _client(os.environ.get("AUTH_COOKIE", ""))
bot_client = _client(os.environ.get("BOT_AUTH_COOKIE", ""))
alpha_client = _client(os.environ.get("ALPHA_AUTH_COOKIE", ""), "alpha.")
