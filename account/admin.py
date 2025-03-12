from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "phone_number",
        "address",
        "dni",
        "created_at",
        "updated_at",
        "is_staff",
        "internal_user",
        "is_superuser"
    ]
    search_fields = ["username", "email", "phone_number", "address", "dni"]
    list_filter = ["created_at", "updated_at", "is_staff", "internal_user", "is_superuser"]
    ordering = ["created_at"]
    list_per_page = 25
    list_display_links = ["username"]

    show_facets = admin.ShowFacets.ALWAYS 

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "address", "dni")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "internal_user", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )
