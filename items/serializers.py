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
            "cooking_level",
            "base_yield_minutes",
            "min_mailable_level",
            "reg_weight",
            "runecube_weight",
            "cooking_recipe_item",
        ]

    def to_internal_value(self, data):
        data["cooking_recipe_item"] = (
            None if data["cooking_recipe_id"] == 0 else data["cooking_recipe_id"]
        )
        # Until this is exposed in the API.
        data["manual_fishing_only"] = data["name"] in Item.MANUAL_FISHING_ONLY
        return super().to_internal_value(data)
