from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from .models import NPC, NPCItem, NPCReward


class NPCItemInline(admin.TabularInline):
    model = NPCItem
    extra = max_num = 0
    can_delete = False
    readonly_fields = [
        "relationship",
        "item",
    ]
    ordering = [
        "relationship",
        "item",
    ]

    def has_add_permission(self, request: HttpRequest, obj: NPCItem) -> bool:
        return False


class NPCRewardInline(admin.TabularInline):
    model = NPCReward
    extra = 1
    raw_id_fields = ["item"]


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ["name", "admin_inline_image"]
    search_fields = ["id", "name"]
    inlines = [NPCItemInline, NPCRewardInline]
    fields = ["name", "short_name", "image"]
    readonly_fields = ["name", "image"]

    @admin.display(description="image")
    def admin_inline_image(self, npc: NPC):
        return format_html('<img src="https://farmrpg.com{}" />', npc.image)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: NPC | None = None
    ) -> bool:
        return False
