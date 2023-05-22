import datetime
from zoneinfo import ZoneInfo
import structlog

from utils.http import client

from .models import Trade, TradeHistory
from .parsers import parse_exchange_center

SERVER_TIME = ZoneInfo("America/Chicago")


log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_all_from_html():
    resp = await client.get("/exchange.php")
    resp.raise_for_status()
    # Compute the time for EC purposes.
    now = datetime.datetime.now(tz=SERVER_TIME).replace(
        minute=0, second=0, microsecond=0
    )
    now = now.replace(hour=12 if now.hour >= 12 else 0)
    for parsed_trade in parse_exchange_center(resp.content):
        trade, _ = await Trade.objects.aget_or_create(
            input_item_id=parsed_trade.input_item,
            input_quantity=parsed_trade.input_quantity,
            output_item_id=parsed_trade.output_item,
            output_quantity=parsed_trade.output_quantity,
            oneshot=parsed_trade.oneshot,
            defaults={"first_seen": now, "last_seen": now},
        )
        if trade.last_seen != now:
            await Trade.objects.filter(id=trade.id).aupdate(last_seen=now)
        await TradeHistory.objects.aget_or_create(trade=trade, seen_at=now)
