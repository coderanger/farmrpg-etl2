from django.contrib import admin

from utils.admin import ReadOnlyAdmin

from .models import BorgenItem


@admin.register(BorgenItem)
class TradeAdmin(ReadOnlyAdmin):
    list_display = [
        "date",
        "item",
        "price",
    ]
