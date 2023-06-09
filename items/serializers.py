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
        ]

    def to_internal_value(self, data):
        data["cooking_recipe_item"] = (
            None if data["cooking_recipe_id"] == 0 else data["cooking_recipe_id"]
        )
        return super().to_internal_value(data)
