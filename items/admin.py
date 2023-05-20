from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.html import format_html

from utils.admin import ReadOnlyAdmin

from .models import Item, WishingWellItem


class WishingWellItemInline(admin.TabularInline):
    model = WishingWellItem
    readonly_fields = ["output_item", "chance"]
    extras = 0
    fk_name = "input_item"

    def has_add_permission(
        self, request: HttpRequest, obj: WishingWellItem | None = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: WishingWellItem | None = None
    ) -> bool:
        return False


@admin.register(Item)
class ItemAdmin(ReadOnlyAdmin):
    list_display = ["id", "name", "admin_inline_image", "created_at"]
    search_fields = ["id", "name"]
    inlines = [WishingWellItemInline]

    @admin.display(description="image")
    def admin_inline_image(self, item: Item):
        return format_html('<img src="https://farmrpg.com{}" />', item.image)
