from django.contrib import admin

from ..utils.admin import ReadOnlyAdmin

from .models import CommunityCenter


@admin.register(CommunityCenter)
class CommunityCenterAdmin(ReadOnlyAdmin):
    list_display = [
        "date",
        "input_item",
        "output_item",
    ]
