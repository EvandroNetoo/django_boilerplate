from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group

from accounts.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    model = User
    add_form_template = ''
    search_fields = ['email']
    list_filter = ['is_superuser']
    list_display = ['email']
    list_display_links = ['email']
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    ordering = ['email']
    fieldsets = (
        (
            'Informações de login',
            {
                'fields': (
                    'email',
                    'password',
                )
            },
        ),
        (
            'Permissões',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
        (
            'Datas importantes',
            {
                'fields': (
                    'last_login',
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            'Informações de login',
            {
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
