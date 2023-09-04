from django.contrib import admin

from ..utils.admin import ReadOnlyAdmin

from .models import Update


@admin.register(Update)
class UpdateAdmin(ReadOnlyAdmin):
    list_display = ["date"]
    search_fields = ["date", "content"]
