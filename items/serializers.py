from rest_framework import serializers

from .models import Item


class ItemAPISerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    img = serializers.CharField(source="image")
    mailable = serializers.BooleanField(source="can_mail")
    craftable = serializers.BooleanField(source="can_craft")
    cookable = serializers.BooleanField(source="can_cook")
    masterable = serializers.BooleanField(source="can_master")
    manfish_only = serializers.BooleanField(source="manual_fishing_only")
    loot_rand = serializers.BooleanField(source="locksmith_grab_bag")
    loot_gold = serializers.IntegerField(source="locksmith_gold")
    loot = serializers.BooleanField(source="can_locksmith")
    event = serializers.BooleanField(source="from_event")
    fm_buy = serializers.BooleanField(source="can_flea_market")
    fm_price = serializers.IntegerField(source="flea_market_price")
    fm_rotate = serializers.BooleanField(source="flea_market_rotate")

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
            "cookable",
            "masterable",
            "description",
            "buy_price",
            "sell_price",
            "crafting_level",
            "cooking_level",
            "base_yield_minutes",
            "min_mailable_level",
            "reg_weight",
            "runecube_weight",
            "cooking_recipe_item",
            "manfish_only",
            "loot_rand",
            "loot_gold",
            "loot",
            "event",
            "fm_buy",
            "fm_price",
            "fm_rotate",
            "locksmith_key",
        ]

    def to_internal_value(self, data):
        data["cooking_recipe_item"] = (
            None if data["cooking_recipe_id"] == 0 else data["cooking_recipe_id"]
        )
        data["locksmith_key"] = (
            None if data["loot_key_id"] == 0 else data["loot_key_id"]
        )
        return super().to_internal_value(data)
