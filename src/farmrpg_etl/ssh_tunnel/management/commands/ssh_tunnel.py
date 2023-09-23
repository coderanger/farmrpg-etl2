import asyncio

from django.core.management.base import BaseCommand

from ...tunnel import connect


class Command(BaseCommand):
    help = "Open an SSH tunnel"

    def handle(self, *args, **options):
        try:
            asyncio.run(self._handle())
        except KeyboardInterrupt:
            pass

    async def _handle(self):
        await connect()
        self.stdout.write("SSH tunnels open")
        while True:
            await asyncio.sleep(1)
