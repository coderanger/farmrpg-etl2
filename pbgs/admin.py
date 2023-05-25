from django.contrib import admin
from django.utils.html import format_html

from .models import ProfileBackground


@admin.register(ProfileBackground)
class ProfileBackgroundAdmin(admin.ModelAdmin):
    list_display = ["name", "game_id", "cost_known"]
    raw_id_fields = ["cost_item"]
    fields = [
        "game_id",
        "name",
        "light_image",
        "light_image_image",
        "dark_image",
        "dark_image_image",
        "cost_silver",
        "cost_gold",
        "cost_item",
        "cost_item_quantity",
    ]
    readonly_fields = [
        "name",
        "light_image_image",
        "dark_image_image",
    ]

    @admin.display(description="Light Image")
    def light_image_image(self, pbg: ProfileBackground) -> str:
        return format_html(
            '<img src="https://farmrpg.com{}" width="256" height="256" />',
            pbg.light_image,
        )

    @admin.display(description="Dark Image")
    def dark_image_image(self, pbg: ProfileBackground) -> str:
        return format_html(
            '<img src="https://farmrpg.com{}" width="256" height="256" />',
            pbg.dark_image,
        )

    @admin.display(description="Cost Known", boolean=True)
    def cost_known(self, pbg: ProfileBackground) -> bool:
        return (
            pbg.cost_silver is not None
            or pbg.cost_gold is not None
            or (pbg.cost_item is not None and pbg.cost_item_quantity is not None)
        )
