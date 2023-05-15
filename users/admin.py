from django.contrib import admin

from utils.admin import ReadOnlyAdmin

from .models import User, UserEvent


@admin.register(User)
class UserAdmin(ReadOnlyAdmin):
    list_display = ["username", "id"]
    search_fields = ["username", "id"]

    fields = ["id", "username", "past_usernames"]

    @admin.display(description="Past Usernames")
    def past_usernames(self, user: User) -> str:
        usernames = (
            UserEvent.objects.filter(user_id=user.id)
            .values_list("username", flat=True)
            .distinct()
        )
        usernames.delete(user.username)
        if not usernames:
            return "-"
        return ", ".join(sorted(usernames))
