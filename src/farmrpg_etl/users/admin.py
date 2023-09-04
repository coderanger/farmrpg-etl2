from django.contrib import admin

from ..utils.admin import ReadOnlyAdmin

from .models import User, UserEvent


@admin.register(User)
class UserAdmin(ReadOnlyAdmin):
    list_display = ["username", "id"]
    search_fields = ["username", "id"]

    fields = ["id", "username", "past_usernames"]

    @admin.display(description="Past Usernames")
    def past_usernames(self, user: User) -> str:
        usernames = list(
            UserEvent.objects.filter(id=user.id)
            .exclude(username=user.username)
            .values_list("username", flat=True)
            .distinct()
        )
        if not usernames:
            return "-"
        return ", ".join(sorted(usernames))
