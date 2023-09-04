from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Password, PasswordGroup, PasswordItem


class PasswordInline(admin.TabularInline):
    model = Password
    extra = 0


@admin.register(PasswordGroup)
class PasswordGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [PasswordInline]


class PasswordItemInline(admin.TabularInline):
    model = PasswordItem
    extra = 0
    readonly_fields = ["item", "quantity"]


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ["password", "group", "has_all_clues", "reward"]
    list_editable = ["group"]
    readonly_fields = [
        "password",
        "reward_silver",
        "reward_gold",
    ]
    inlines = [PasswordItemInline]

    @admin.display(description="Has All Clues", boolean=True)
    def has_all_clues(self, password: Password) -> bool:
        return bool(password.clue1 and password.clue2 and password.clue3)

    @admin.display(description="Reward")
    def reward(self, password: Password) -> str:
        parts = []
        if password.reward_silver:
            parts.append(format_html("Silver x{}", password.reward_silver))
        if password.reward_gold:
            parts.append(format_html("Gold x{}", password.reward_gold))
        for item in password.reward_items.all().select_related("item"):
            parts.append(format_html("{} x{}", item.item.name, item.quantity))
        return mark_safe("<br>".join(parts))
