from django.contrib import admin
from django.http import HttpRequest

from .models import NPC, NPCItem, NPCReward


class NPCItemInline(admin.TabularInline):
    model = NPCItem
    extra = 0
    can_delete = False
    template = "admin_tabular_inline_no_origin.html"
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
    template = "admin_tabular_inline_no_origin.html"
    raw_id_fields = ["item"]


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["id", "name"]
    inlines = [NPCItemInline, NPCRewardInline]
    fields = ["name", "short_name", "image"]
    readonly_fields = ["name", "image"]
