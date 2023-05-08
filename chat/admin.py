from django.contrib import admin

from utils.admin import ReadOnlyAdmin

from .models import Emblem


@admin.register(Emblem)
class EmblemAdmin(ReadOnlyAdmin):
    list_display = ["name", "keywords"]
    search_fields = ["name", "keywords"]
