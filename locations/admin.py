from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from .models import Location, LocationItem


class LocationItemInline(admin.TabularInline):
    model = LocationItem
    extra = 0
    readonly_fields = [
        "location",
        "item",
        "sometimes",
    ]


@admin.register(Location)
class QuestAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "game_id",
    ]
    search_fields = ["game_id", "name"]
    inlines = [LocationItemInline]
    fields = [
        "type",
        "game_id",
        "name",
        "image",
        "base_drop_rate",
    ]
    readonly_fields = [
        "game_id",
        "type",
        "name",
        "image",
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
