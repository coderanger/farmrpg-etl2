import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo

from rest_framework import serializers

from .models import Quest

SERVER_TIME = ZoneInfo("America/Chicago")


def parse_date(value: str, hour: int = 0, minute: int = 0, second: int = 0) -> datetime:
    if value == "0000-00-00":
        return None
    year, month, day = value.split("-")
    return datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=SERVER_TIME,
    )


class QuestAPISerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Quest
        fields = [
            "id",
            "npc",
            "npc_img",
            "title",
            "author",
            "pred",
            "start_date",
            "end_date",
            "main_quest",
            "description",
            "required_silver",
            "required_farming_level",
            "required_fishing_level",
            "required_crafting_level",
            "required_exploring_level",
            "required_cooking_level",
            "required_tower_level",
            "required_npc_id",
            "required_npc_level",
            "reward_silver",
            "reward_gold",
            "completed_count",
        ]

    def to_internal_value(self, data):
        data["start_date"] = parse_date(data["start_date"])
        data["end_date"] = parse_date(data["end_date"], hour=23, minute=59, second=59)
        if data["author"] == "":
            data["author"] = None
        data["pred"] = None if data["pred_id"] == 0 else data["pred_id"]
        data["npc_img"] = urllib.parse.urljoin(
            "/img/items/", data.get("npc_img") or "missing.png"
        )
        return super().to_internal_value(data)
