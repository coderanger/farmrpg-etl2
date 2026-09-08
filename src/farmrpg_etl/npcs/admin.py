from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from .models import NPC, NPCItem, NPCReward, NPCSpecialItem


class NPCItemInline(admin.TabularInline):
    model = NPCItem
    extra = max_num = 0
    can_delete = False
    readonly_fields = [
        "relationship",
        "item",
        "special_xp",
    ]
    ordering = [
        "relationship",
        "item",
        "special_xp",
    ]

    def has_add_permission(self, request: HttpRequest, obj: NPCItem) -> bool:
        return False


class NPCRewardInline(admin.TabularInline):
    model = NPCReward
    extra = max_num = 0
    can_delete = False
    readonly_fields = [
        "level",
        "order",
        "item",
        "quantity",
    ]
    ordering = [
        "level",
        "order",
    ]


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ["name", "admin_inline_image", "is_available"]
    search_fields = ["id", "name"]
    inlines = [NPCItemInline, NPCRewardInline]
    fields = ["name", "short_name", "image", "is_available"]
    readonly_fields = ["name", "image", "is_available"]

    @admin.display(description="image")
    def admin_inline_image(self, npc: NPC):
        return format_html('<img src="https://farmrpg.com{}" />', npc.image)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: NPC | None = None
    ) -> bool:
        return False


@admin.register(NPCSpecialItem)
class NPCSpecialItemAdmin(admin.ModelAdmin):
    list_display = ["item_name", "npc_name", "relationship", "special_xp"]
    list_select_related = ["item", "npc"]
    fields = ["item", "npc", "relationship", "special_xp"]
    raw_id_fields = ["item"]

    @admin.display(description="Item")
    def item_name(self, obj: NPCSpecialItem) -> str:
        return obj.item.name

    @admin.display(description="NPC")
    def npc_name(self, obj: NPCSpecialItem) -> str:
        return obj.npc.name
