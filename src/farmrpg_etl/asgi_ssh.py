"""
ASGI config for farmrpg-etl project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import asyncio
import os

import structlog
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmrpg_etl.settings")

from .ssh_tunnel.tunnel import connect

ssh_lock = asyncio.Lock()
_application = None
log = structlog.stdlib.get_logger(mod="asgi")


async def application(scope, receive, send):
    global _application
    async with ssh_lock:
        if _application is None:
            await connect()
            log.info("SSH tunnels open")
            _application = get_asgi_application()
    await _application(scope, receive, send)
