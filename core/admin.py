from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from profiles.models import Profile

class CustomUserAdmin(UserAdmin):
    """
    Customizes the Django admin panel for the User model.

    Extends the default UserAdmin class to include additional
    functionality, specifically the display of user roles (groups)
    in the admin interface.
    """
    # Extending the list of displayed fields to include "get_roles"
    list_display = UserAdmin.list_display + ('get_roles',)

    def get_roles(self, obj):
        """
        Retrieves a comma-seperated string of role names (groups)
        that a user belongs to.

        Args:
            obj: The user instance being displayed in the admin.

        Returns: 
            str: A string containing the names of all groups the
                 user belongs to, seperated by commas.
        """
        return ', '.join([group.name for group in obj.groups.all()])
    
    # Sets the column title in the admin panel for the 'get_roles'.
    get_roles.short_description = 'Roles'

class ProfileAdmin(admin.ModelAdmin):
        list_display = ('user', 'bio', 'avatar')  # Πεδία που θα εμφανίζονται
        fields = ('user', 'bio', 'avatar')  # Πεδία που μπορεί να επεξεργαστεί ο admin
        readonly_fields = ('user',)
    
# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile, ProfileAdmin)

