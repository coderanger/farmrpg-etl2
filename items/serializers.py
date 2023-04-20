from rest_framework import serializers

from .models import Item


class ItemAPISerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    img = serializers.CharField(source="image")
    mailable = serializers.BooleanField(source="can_mail")
    craftable = serializers.BooleanField(source="can_craft")
    masterable = serializers.BooleanField(source="can_master")

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "img",
            "type",
            "xp",
            "can_buy",
            "can_sell",
            "mailable",
            "craftable",
            "masterable",
            "description",
            "buy_price",
            "sell_price",
            "crafting_level",
            "base_yield_minutes",
            "min_mailable_level",
        ]
