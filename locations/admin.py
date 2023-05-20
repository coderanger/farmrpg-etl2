from typing import Any

from django.contrib import admin
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from .models import DropRates, DropRatesItem, Location, LocationItem


class LocationItemInline(admin.TabularInline):
    model = LocationItem
    extra = 0
    can_delete = False
    readonly_fields = [
        "location",
        "item",
        "sometimes",
    ]

    def has_add_permission(self, request: HttpRequest, obj: DropRates) -> bool:
        return False


class DropRatesInline(admin.TabularInline):
    model = DropRates
    extra = 0
    can_delete = False
    fields = readonly_fields = [
        "link",
        "iron_depot",
        "manual_fishing",
        "runecube",
    ]

    def has_add_permission(self, request: HttpRequest, obj: DropRates) -> bool:
        return False

    @admin.display(description="Link")
    def link(self, obj: DropRates) -> str:
        return format_html(
            '<a href="{}">View</a>',
            reverse("admin:locations_droprates_change", args=(obj.pk,)),
        )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "game_id",
    ]
    search_fields = ["game_id", "name"]
    inlines = [LocationItemInline, DropRatesInline]
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


class DropRatesItemInline(admin.TabularInline):
    model = DropRatesItem
    extra = 0
    can_delete = False
    fields = [
        "item",
        "rate",
    ]
    readonly_fields = [
        "item",
    ]

    def has_add_permission(self, request: HttpRequest, obj: DropRates) -> bool:
        return False


@admin.register(DropRates)
class DropRatesAdmin(admin.ModelAdmin):
    list_display = [
        "for_",
        "runecube",
        "iron_depot",
        "manual_fishing",
    ]
    readonly_fields = [
        "location",
        "seed",
        "iron_depot",
        "manual_fishing",
        "runecube",
        "hash",
        "compute_time",
    ]
    inlines = [DropRatesItemInline]

    @admin.display(description="For")
    def for_(self, obj: DropRates) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:locations_droprates_change", args=(obj.pk,)),
            obj.location or obj.seed,
        )
