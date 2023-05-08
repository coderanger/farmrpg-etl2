from django.contrib import admin

from utils.admin import ReadOnlyAdmin

from .models import Quest, QuestItemRequired, QuestItemReward


class QuestItemRequiredInline(admin.TabularInline):
    model = QuestItemRequired
    extra = 0
    template = "admin_tabular_inline_no_origin.html"


class QuestItemRewardInline(admin.TabularInline):
    model = QuestItemReward
    extra = 0
    template = "admin_tabular_inline_no_origin.html"


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
