import json
from datetime import datetime

import firebase_admin
import httpx

app = firebase_admin.initialize_app()

_auth_token_cache: list[firebase_admin.credentials.AccessTokenInfo] = []


def _google_auth_token() -> str:
    if not _auth_token_cache or _auth_token_cache[0].expiry >= datetime.now():
        # Need a new token.
        _auth_token_cache.clear()
        _auth_token_cache.append(app.credential.get_access_token())
    return _auth_token_cache[0].access_token


async def _add_token(request: httpx.Request):
    request.headers["Authorization"] = f"Bearer {_google_auth_token()}"


google_client = httpx.AsyncClient(event_hooks={"request": [_add_token]})


async def set_custom_user_claims(uid: str, claims: dict[str, str]) -> httpx.Response:
    resp = await google_client.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:update",
        json={
            "localId": uid,
            "customAttributes": json.dumps(claims),
        },
    )
    resp.raise_for_status()
    return resp
