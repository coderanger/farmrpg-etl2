from django.contrib import admin

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
    list_display = ["password", "has_all_clues"]
    readonly_fields = [
        "password",
        "reward_silver",
        "reward_gold",
    ]
    inlines = [PasswordItemInline]

    @admin.display(description="Has All Clues", boolean=True)
    def has_all_clues(self, password: Password) -> bool:
        return bool(password.clue1 and password.clue2 and password.clue3)
