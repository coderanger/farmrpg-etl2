from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.html import format_html


from .models import (
    Item,
    LocksmithItem,
    ManualProduction,
    RecipeItem,
    SkillLevelReward,
    WishingWellItem,
)


class LocksmithItemInline(admin.TabularInline):
    model = LocksmithItem
    fk_name = "item"

    def has_add_permission(self, request: HttpRequest, obj: Item | None = None) -> bool:
        return obj.locksmith_grab_bag

    def has_delete_permission(
        self, request: HttpRequest, obj: Item | None = None
    ) -> bool:
        return obj.locksmith_grab_bag

    def get_readonly_fields(
        self, request: HttpRequest, obj: Item | None = None
    ) -> list[str]:
        return (
            []
            if obj.locksmith_grab_bag
            else ["output_item", "quantity_min", "quantity_max"]
        )

    def get_extra(self, request: HttpRequest, obj: Item | None = None) -> int:
        return 1 if obj.locksmith_grab_bag else 0


class RecipeItemInline(admin.TabularInline):
    model = RecipeItem
    readonly_fields = ["ingredient_item", "quantity"]
    extra = 0
    fk_name = "item"

    def has_add_permission(
        self, request: HttpRequest, obj: RecipeItem | None = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: RecipeItem | None = None
    ) -> bool:
        return False


class WishingWellItemInline(admin.TabularInline):
    model = WishingWellItem
    readonly_fields = ["output_item", "chance"]
    extra = 0
    fk_name = "input_item"

    def has_add_permission(
        self, request: HttpRequest, obj: WishingWellItem | None = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: WishingWellItem | None = None
    ) -> bool:
        return False


class ManualProductionInline(admin.TabularInline):
    model = ManualProduction
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "admin_inline_image", "created_at"]
    search_fields = ["id", "name"]
    fields = [
        "name",
        "image",
        "type",
        "xp",
        "can_buy",
        "can_sell",
        "can_mail",
        "can_craft",
        "can_master",
        "description",
        "buy_price",
        "sell_price",
        "crafting_level",
        "cooking_level",
        "base_yield_minutes",
        "min_mailable_level",
        "reg_weight",
        "runecube_weight",
        "locksmith_grab_bag",
        "locksmith_key",
        "locksmith_gold",
        "cooking_recipe_item",
        "manual_fishing_only",
    ]
    readonly_fields = [
        "name",
        "image",
        "type",
        "xp",
        "can_buy",
        "can_sell",
        "can_mail",
        "can_craft",
        "can_master",
        "description",
        "buy_price",
        "sell_price",
        "crafting_level",
        "cooking_level",
        "base_yield_minutes",
        "min_mailable_level",
        "reg_weight",
        "runecube_weight",
        "locksmith_gold",
        "cooking_recipe_item",
        "manual_fishing_only",
    ]
    raw_id_fields = [
        "locksmith_key",
    ]
    inlines = [
        LocksmithItemInline,
        RecipeItemInline,
        WishingWellItemInline,
        ManualProductionInline,
    ]

    @admin.display(description="image")
    def admin_inline_image(self, item: Item):
        return format_html('<img src="https://farmrpg.com{}" />', item.image)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Item | None = None
    ) -> bool:
        return False


@admin.register(SkillLevelReward)
class SkillLevelRewardAdmin(admin.ModelAdmin):
    list_display = ["skill", "level", "order", "admin_reward"]
    list_filter = ["skill"]
    search_fields = ["skill", "level"]
    raw_id_fields = ["item"]

    @admin.display(description="Reward")
    def admin_reward(self, obj: SkillLevelReward) -> str:
        if obj.silver is not None:
            return f"Silver (x{obj.silver})"
        elif obj.gold is not None:
            return f"Gold (x{obj.gold})"
        elif obj.ak is not None:
            return f"AK (x{obj.ak})"
        else:
            return f"{obj.item.name} (x{obj.item_quantity})"
