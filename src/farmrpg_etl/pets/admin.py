from typing import Any

from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest

from ..items.models import Item

from .models import Pet, PetItem


class PetItemInline(admin.TabularInline):
    model = PetItem
    extra = 0

    def formfield_for_foreignkey(
        self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any
    ) -> ModelChoiceField | None:
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "item":
            field.queryset = Item.objects.all().order_by("name")
        return field


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["game_id", "name"]
    search_fields = ["game_id", "name"]
    inlines = [PetItemInline]
