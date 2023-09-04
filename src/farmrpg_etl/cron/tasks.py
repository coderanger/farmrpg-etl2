import asyncio
import traceback
from datetime import datetime, time
from datetime import timezone as dtimezone
from zoneinfo import ZoneInfo

import sentry_sdk
import structlog
from croniter import croniter
from django.utils import timezone
from django.utils.module_loading import autodiscover_modules

from . import decorators
from .decorators import CronRegistration
from .models import Cron

SERVER_TIME = ZoneInfo("America/Chicago")
MAINTENANCE_START = time(23, 29)
MAINTENANCE_END = time(23, 36)

log = structlog.stdlib.get_logger(mod=__name__)


async def _process_one_cron(cron: CronRegistration) -> None:
    # Save the before state stuff.
    model = await cron.model()
    await model.asave(update_fields=["previous_started_at"])
    # Run the task.
    log.debug("Starting cron", name=cron.name)
    try:
        # TODO output capture
        value = await cron.fn()
    except Exception as exc:
        log.error("Error in cron", exc_info=True, name=cron.name)
        sentry_sdk.capture_exception(exc)
        model.previous_error = traceback.format_exc()
    else:
        log.debug("Finished cron", name=cron.name, value=value)
        model.previous_error = None
    now = timezone.now()
    model.previous_finished_at = now
    model.next_run_at = (
        croniter(cron.cronspec, now, hash_id=cron.name)
        .get_next(ret_type=datetime)
        .replace(tzinfo=dtimezone.utc)
    )
    log.debug("Next cron run scheduled", name=cron.name, at=model.next_run_at)
    await model.asave(
        update_fields=["previous_error", "previous_finished_at", "next_run_at"]
    )


async def process_cron() -> None:
    # Clean up any cron records in the DB which don't exist anymore.
    await Cron.objects.exclude(name__in=decorators._registry).adelete()
    # Reset all times.
    await Cron.objects.all().aupdate(next_run_at=None, previous_started_at=None)

    while True:
        now = timezone.now()

        # Don't run any background tasks during maintenance, most will just fail.
        if MAINTENANCE_START <= now.astimezone(SERVER_TIME).time() <= MAINTENANCE_END:
            await asyncio.sleep(60)
            continue

        for cron in decorators._registry.values():
            model = await cron.model()
            # log.debug(
            #     "Evaulating cron",
            #     name=cron.name,
            #     next_run_at=model.next_run_at,
            #     previous_started_at=model.previous_started_at,
            #     previous_finished_at=model.previous_finished_at,
            # )
            if (model.next_run_at is None or model.next_run_at <= now) and (
                model.previous_started_at is None
                or (
                    model.previous_finished_at is not None
                    and model.previous_started_at <= model.previous_finished_at
                )
            ):
                model.previous_started_at = now
                asyncio.create_task(
                    _process_one_cron(cron),
                    name=f"process_one_cron_{cron.name}_{now}",
                )
        await asyncio.sleep(1)


def start_cron() -> None:
    # Check if we're in an async context.
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return

    # Try to import a .tasks module from all installed apps.
    autodiscover_modules("tasks", register_to=decorators)

    asyncio.create_task(process_cron(), name="process_cron")
