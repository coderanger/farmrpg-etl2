from django.contrib import admin
from django.utils.html import format_html

from utils.admin import ReadOnlyAdmin

from .models import Item


@admin.register(Item)
class ItemAdmin(ReadOnlyAdmin):
    list_display = ["id", "name", "admin_inline_image", "created_at"]
    search_fields = ["id", "name"]

    @admin.display(description="image")
    def admin_inline_image(self, item: Item):
        return format_html('<img src="https://farmrpg.com{}" />', item.image)
