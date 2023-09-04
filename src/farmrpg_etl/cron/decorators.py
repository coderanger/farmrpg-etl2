import fnmatch
from collections.abc import Awaitable, Callable
from typing import TypeVar

import attrs
import structlog
from croniter import croniter
from django.conf import settings

from .models import Cron

log = structlog.stdlib.get_logger(mod=__name__)

RV = TypeVar("RV")
Cronable = Callable[[], Awaitable[RV]]


@attrs.define
class CronRegistration:
    name: str
    cronspec: str
    fn: Cronable
    _model: Cron | None = None

    async def model(self) -> Cron:
        cron = getattr(self, "_model", None)
        if cron is None:
            cron, _ = await Cron.objects.aupdate_or_create(
                name=self.name, defaults={"cronspec": self.cronspec}
            )
            self._model = cron
        return cron


_registry: dict[str, CronRegistration] = {}


def cron(cronspec: str, name: str | None = None) -> Callable[[Cronable], Cronable]:
    if not croniter.is_valid(cronspec, hash_id=b""):
        raise ValueError(f"{cronspec} is not a valid cronspec")

    def dectorator(fn: Cronable) -> Cronable:
        reg = CronRegistration(
            name=name or fn.__name__,
            cronspec=cronspec,
            fn=fn,
        )

        # Check if we should register this cron.
        if any(fnmatch.fnmatch(reg.name, t) for t in settings.ENABLE_TASKS):
            log.info("Registering cron", name=reg.name)
            assert reg.name not in _registry
            _registry[reg.name] = reg
        else:
            log.info("Not registering cron due to settings", name=reg.name)

        return fn

    return dectorator
