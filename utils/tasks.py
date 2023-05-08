import asyncio
import fnmatch
from asyncio import Task
from datetime import datetime, time
from typing import Any, Callable, Coroutine
from zoneinfo import ZoneInfo

import attrs
import sentry_sdk
import structlog
from django.conf import settings

SERVER_TIME = ZoneInfo("America/Chicago")
MAINTENANCE_START = time(23, 29)
MAINTENANCE_END = time(23, 36)

log = structlog.stdlib.get_logger(mod="tasks")


@attrs.define
class PeriodicTask:
    _task: Task
    _is_stopping: list[bool]

    def stop(self) -> None:
        self._is_stopping[0] = True

    def __getattribute__(self, name: str) -> Any:
        return getattr(self._task, name)


def create_periodic_task(
    coro: Callable[[], Coroutine], interval: int | float, *, name: str | None = None
):
    # Check if we're in an async context.
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return

    if name is not None and not any(
        fnmatch.fnmatch(name, t) for t in settings.ENABLE_TASKS
    ):
        log.info("Not creating task due to settings", name=name)
        return

    is_stopping = [False]
    if name is None:
        name = coro.__name__

    async def wrapper():
        while not is_stopping[0]:
            # Don't run any background tasks during maintenance, most will just fail.
            now = datetime.now(SERVER_TIME).time()
            if MAINTENANCE_START <= now <= MAINTENANCE_END:
                await asyncio.sleep(60)
                continue

            try:
                await coro()
            except Exception as exc:
                log.error("Error in periodic task", exc_info=True, task_name=name)
                sentry_sdk.capture_exception(exc)
            await asyncio.sleep(interval)

    task = asyncio.create_task(wrapper(), name=name)
    return PeriodicTask(task, is_stopping)


class FakeSemaphore:
    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        pass


class AsyncPool:
    def __init__(self, max_concurrency: int | None = None) -> None:
        self.tasks = []
        self.max_concurrency = max_concurrency
        self._semaphore = (
            FakeSemaphore()
            if max_concurrency is None
            else asyncio.Semaphore(max_concurrency)
        )

    def add(self, coro: Coroutine, name: str | None = None) -> None:
        async def wrapper():
            async with self._semaphore:
                await coro

        task = asyncio.create_task(wrapper(), name=name)
        self.tasks.append(task)

    async def wait(self):
        await asyncio.wait(self.tasks)
