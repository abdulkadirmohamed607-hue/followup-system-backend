from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'first_name',
        'last_name',
        'phone',
        'role',
        'must_change_password',
        'is_active',
    )

    list_filter = (
        'role',
        'is_active',
        'must_change_password',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'phone',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'FollowUp System Information',
            {
                'fields': (
                    'phone',
                    'role',
                    'must_change_password',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'FollowUp System Information',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone',
                    'role',
                    'must_change_password',
                )
            },
        ),
    )