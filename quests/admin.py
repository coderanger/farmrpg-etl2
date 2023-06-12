from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.html import format_html

from utils.admin import ReadOnlyAdmin

from .models import Quest, QuestItemRequired, QuestItemReward, Questline, QuestlineStep


class QuestItemRequiredInline(admin.TabularInline):
    model = QuestItemRequired
    extra = 0
    order_by = ["order"]
    fields = ["item", "quantity"]


class QuestItemRewardInline(admin.TabularInline):
    model = QuestItemReward
    extra = 0
    order_by = ["order"]
    fields = ["item", "quantity"]


@admin.register(Quest)
class QuestAdmin(ReadOnlyAdmin):
    list_display = [
        "id",
        "title",
        "created_at",
        "required_farming_level",
        "required_fishing_level",
        "required_crafting_level",
        "required_exploring_level",
    ]
    search_fields = ["id", "title"]
    inlines = [QuestItemRequiredInline, QuestItemRewardInline]


class QuestlineStepInline(admin.TabularInline):
    model = QuestlineStep
    raw_id_fields = ["quest"]
    extra = 1

    # def get_extra(self, request: HttpRequest, obj: Questline | None = None) -> int:
    #     return 0 if obj.automatic else 1

    def get_readonly_fields(
        self, request: HttpRequest, obj: Questline | None = None
    ) -> list[str]:
        return ["order", "quest"] if obj.automatic else []

    def has_add_permission(
        self, request: HttpRequest, obj: Questline | None = None
    ) -> bool:
        return not obj.automatic

    def has_delete_permission(
        self, request: HttpRequest, obj: Questline | None = None
    ) -> bool:
        return not obj.automatic


@admin.register(Questline)
class QuestlineAdmin(admin.ModelAdmin):
    list_display = ["title", "automatic", "admin_inline_image", "admin_quest_count"]
    search_fields = ["title"]
    fields = [
        "title",
        "image",
        "automatic",
    ]
    inlines = [QuestlineStepInline]

    @admin.display(description="image")
    def admin_inline_image(self, obj: Questline) -> str:
        return format_html('<img src="https://farmrpg.com/img/items/{}" />', obj.image)

    @admin.display(description="# of Quests")
    def admin_quest_count(self, obj: Questline) -> int:
        return obj.steps.count()

    def get_readonly_fields(
        self, request: HttpRequest, obj: Questline | None = None
    ) -> list[str]:
        return ["title", "image"] if obj.automatic else []
