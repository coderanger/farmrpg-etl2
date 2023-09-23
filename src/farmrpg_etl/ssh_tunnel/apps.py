import asyncio

import structlog
from django.apps import AppConfig

from .tunnel import connect

log = structlog.stdlib.get_logger(mod=__name__)


class SshTunnelConfig(AppConfig):
    name = "farmrpg_etl.ssh_tunnel"

    def ready(self) -> None:
        async def _connect():
            await connect()
            log.info("SSH tunnels open")

        asyncio.create_task(_connect(), name="ssh-tunnel-connect")
