from django.contrib import admin

from utils.admin import ReadOnlyAdmin

from .models import Quiz, QuizAnswer, QuizReward


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 0
    template = "admin_tabular_inline_no_origin.html"


class QuizRewardInline(admin.TabularInline):
    model = QuizReward
    extra = 0
    template = "admin_tabular_inline_no_origin.html"


@admin.register(Quiz)
class QuizAdmin(ReadOnlyAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
    ]
    search_fields = ["id", "name"]
    inlines = [QuizRewardInline, QuizAnswerInline]
