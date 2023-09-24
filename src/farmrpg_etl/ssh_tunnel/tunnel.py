import enum
import os

import asyncssh


class Server(enum.StrEnum):
    PROD = enum.auto()
    ALPHA = enum.auto()


FORWARD_PORTS = {
    Server.PROD: 3307,
    Server.ALPHA: 3308,
}

_TUNNEL_READY = False


async def _connect_one(server: Server):
    hostname, port = os.environ[f"SSH_{server.upper()}_HOST"].split(":")
    hostkeys = os.environb[f"SSH_{server.upper()}_HOSTKEYS".encode()]
    key = asyncssh.import_private_key(os.environ["SSH_KEY"])
    conn = await asyncssh.connect(
        hostname,
        username="etl",
        port=int(port),
        client_keys=[key],
        keepalive_interval=1,
        known_hosts=hostkeys,
    )
    await conn.forward_local_port("127.0.0.1", FORWARD_PORTS[server], "127.0.0.1", 3306)


def tunnel_is_ready() -> bool:
    return _TUNNEL_READY


async def connect():
    await _connect_one(Server.PROD)
    await _connect_one(Server.ALPHA)
    global _TUNNEL_READY
    _TUNNEL_READY = True
