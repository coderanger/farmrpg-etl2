import datetime
from zoneinfo import ZoneInfo
import structlog

from items.models import Item
from utils.http import client

from .models import Trade, TradeHistory, CardsTrade
from .parsers import parse_cards, parse_exchange_center

SERVER_TIME = ZoneInfo("America/Chicago")


log = structlog.stdlib.get_logger(mod=__name__)


async def scrape_trades_from_html():
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


async def scrape_cards_from_html():
    resp = await client.get("/manage_hoc.php")
    resp.raise_for_status()
    seen_ids = []
    for parsed in parse_cards(resp.content):
        # Find the output item ID.
        log.debug("Updating cards trade", id=parsed.id, output_item=parsed.output_item)
        output_item_id = await Item.objects.values_list("id", flat=True).aget(
            name=parsed.output_item
        )
        trade, _ = await CardsTrade.objects.aupdate_or_create(
            id=parsed.id,
            defaults={
                "spades_quantity": parsed.spades_quantity,
                "hearts_quantity": parsed.hearts_quantity,
                "diamonds_quantity": parsed.diamonds_quantity,
                "clubs_quantity": parsed.clubs_quantity,
                "joker_quantity": parsed.joker_quantity,
                "output_item_id": output_item_id,
                "output_quantity": parsed.output_quantity,
                "is_disabled": False,
            },
        )
        seen_ids.append(trade.pk)
    await CardsTrade.objects.filter(is_disabled=False).exclude(pk__in=seen_ids).aupdate(
        is_disabled=True
    )
