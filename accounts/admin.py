from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "organisation", "is_active")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "organisation", "filiere")
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Informations académiques & professionnelles",
            {"fields": ("role", "telephone", "organisation", "filiere", "niveau", "specialite")},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Rôle et profil",
            {"fields": ("role", "telephone", "organisation", "filiere", "niveau", "specialite")},
        ),
    )
