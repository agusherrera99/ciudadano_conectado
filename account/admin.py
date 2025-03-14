from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Department, ExternalUser, InternalUser,  Position


@admin.register(ExternalUser)
class ExternalUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "phone_number",
        "address",
        "dni",
        "created_at",
        "updated_at",
    ]
    search_fields = ["username", "email", "phone_number", "address", "dni"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["created_at"]
    list_per_page = 25
    list_display_links = ["username"]

    show_facets = admin.ShowFacets.ALWAYS 

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "address", "dni")}),
        ("Permissions", {"fields": ("is_active", "groups")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

@admin.register(InternalUser)
class InternalUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "department",
        "position",
        "created_at",
        "updated_at",
        "get_groups",
        "is_staff",
    ]
    search_fields = ["username", "email", "department__name", "position__name"]
    list_filter = ["department", "position", "created_at", "updated_at", "is_staff"]
    ordering = ["created_at"]
    list_per_page = 25
    list_display_links = ["username"]

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "address", "dni")}),
        ("Departamento", {"fields": ("department", "position")}),
        ("Permissions", {"fields": ("is_active", "groups")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = "Grupos"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def save_model(self, request, obj, form, change):
        obj.is_internal = True  # Asegurar que siempre se guarde como interno
        super().save_model(request, obj, form, change)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_at",
        "updated_at"
    ]
    search_fields = ["name"]
    ordering = ["created_at"]
    list_per_page = 25
    list_display_links = ["name"]

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {"fields": ("name",)}),
    )

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_at",
        "updated_at"
    ]
    search_fields = ["name"]
    ordering = ["created_at"]
    list_per_page = 25
    list_display_links = ["name"]

    show_facets = admin.ShowFacets.ALWAYS

    fieldsets = (
        (None, {"fields": ("name",)}),
    )