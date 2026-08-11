from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Workforce254 Information",
            {
                "fields": (
                    "organization",
                    "role",
                    "phone",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Workforce254 Information",
            {
                "fields": (
                    "email",
                    "organization",
                    "role",
                    "phone",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "organization",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "organization",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )