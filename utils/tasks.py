import asyncio
import fnmatch
from asyncio import Task
from typing import Any, Callable, Coroutine

import attrs
import structlog
from django.conf import settings

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

    if name is not None and any(
        fnmatch.fnmatch(name, t) for t in settings.DISABLE_TASKS
    ):
        log.info("Not creating task due to settings", name=name)
        return

    is_stopping = [False]
    if name is None:
        name = coro.__name__

    async def wrapper():
        while not is_stopping[0]:
            try:
                await coro()
            except Exception:
                log.error("Error in periodic task", exc_info=True, task_name=name)
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
