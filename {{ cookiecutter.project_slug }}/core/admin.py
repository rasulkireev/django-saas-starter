from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    list_display = ["date_joined", "username", "email", "first_name", "last_name"]
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {"fields": ("twitter_handle",)},
        ),
    )


admin.site.register(User, UserAdmin)
