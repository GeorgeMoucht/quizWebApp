from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'avatar')
    fk_name = 'user'
    extra = 0

class CustomUserAdmin(DefaultUserAdmin):
    inlines = (ProfileInline,)

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','get_roles','is_active')

    def get_roles(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_roles.short_description = 'Roles'

# Εγγραφή του Custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
