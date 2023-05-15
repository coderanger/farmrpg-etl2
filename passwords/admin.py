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
    extra = 1
    raw_id_fields = ["item"]


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ["password"]
    inlines = [PasswordItemInline]
