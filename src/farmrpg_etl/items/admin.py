from django.contrib import admin
from django.db.models import Prefetch, QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html

from ..utils.admin import ReadOnlyAdmin

from .models import (
    Item,
    LocksmithItem,
    ManualProduction,
    RecipeItem,
    SkillLevelReward,
    TempleReward,
    TempleRewardItem,
    WishingWellItem,
)


class LocksmithItemInline(admin.TabularInline):
    model = LocksmithItem
    fk_name = "item"
    extra = 0
    readonly_fields = ("output_item", "quantity_min", "quantity_max")

    def has_add_permission(self, request: HttpRequest, obj: Item | None = None) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Item | None = None
    ) -> bool:
        return False


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
        "can_cook",
        "can_master",
        "can_locksmith",
        "can_flea_market",
        "description",
        "buy_price",
        "flea_market_price",
        "flea_market_rotate",
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
        "from_event",
    ]
    readonly_fields = fields
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


class TempleRewardItemInline(admin.TabularInline):
    model = TempleRewardItem
    readonly_fields = ["order", "item", "quantity"]
    extra = 0


@admin.register(TempleReward)
class TempleRewardAdmin(ReadOnlyAdmin):
    list_display = ["input_item", "input_quantity", "admin_reward"]
    search_fields = ["input_item__name", "input_item__id"]
    inlines = [TempleRewardItemInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[TempleReward]:
        qs = super().get_queryset(request)
        if request.resolver_match.view_name.endswith("changelist"):
            return qs.prefetch_related(
                Prefetch(
                    "items", queryset=TempleRewardItem.objects.select_related("item")
                )
            )
        return qs

    @admin.display(description="Reward")
    def admin_reward(self, obj: TempleReward) -> str:
        buf = []
        if obj.silver is not None:
            buf.append(f"Silver (x{obj.silver})")
        if obj.gold is not None:
            buf.append(f"Gold (x{obj.gold})")
        for tri in obj.items.all():
            buf.append(f"{tri.item.name} (x{tri.quantity})")
        return " ".join(buf)
