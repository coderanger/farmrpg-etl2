import collections
import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand

from items.models import Item
from exchange_center.models import Trade, TradeHistory

UTC = ZoneInfo("UTC")
SERVER_TIME = ZoneInfo("America/Chicago")
FIXTURES_ROOT = Path(__file__).joinpath("../../../fixtures").resolve()


class ItemMap(collections.defaultdict):
    def __missing__(self, key: str) -> int:
        return Item.objects.values_list("id", flat=True).get(name=key)


class Command(BaseCommand):
    help = "Load initial passwords data"

    def handle(self, *args, **options):
        item_ids = ItemMap()

        data = json.load(FIXTURES_ROOT.joinpath("backfill.json").open("r"))
        for row in data:
            first_seen = datetime.datetime.fromtimestamp(
                row["firstSeen"] / 1000, tz=UTC
            )
            date_parts = [int(s) for s in row["date"].split("-")]
            date = datetime.datetime(*date_parts, tzinfo=SERVER_TIME)
            trade, created = Trade.objects.get_or_create(
                input_item_id=item_ids[row["giveItem"]],
                input_quantity=row["giveQuantity"],
                output_item_id=item_ids[row["receiveItem"]],
                output_quantity=row["receiveQuantity"],
                oneshot=row["oneShot"],
                defaults={
                    "first_seen": date,
                    "last_seen": date,
                },
            )
            update_fields = []
            if date > trade.last_seen:
                trade.last_seen = date
                update_fields.append("last_seen")
            if date < trade.first_seen:
                trade.first_seen = date
                update_fields.append("first_seen")
            if update_fields:
                trade.save(update_fields=update_fields)
            TradeHistory.objects.get_or_create(trade=trade, seen_at=date)
