from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User, Tag, Ingredient
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):

    ordering = ["id"]
    list_display = ["email", "name"]
    # fields needed for our change page user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
        # fields needed for our add page user
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2')
    }),
)


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)