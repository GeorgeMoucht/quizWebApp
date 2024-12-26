from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    """
    Custom management command to set up default roles in the app.

    This command creates predefined user roles ('Teacher' and 'Student)
    in the Django Group model if they do not already exists.

    Usage:
        python manage.py setup_roles
    """
    help = 'Setup default roles'

    def handle(self, *args, **kwargs):
        """
        Core logic of the command to create default roles.

        Args:
            *args: Variable length argument list (unused in implementation)
            **kwargs: Arbitrary keyword argument (unused in implementation)
        
        Behavior:
            Loops through a predefined list of roles and ensures that
            each role exists in the Group model. If a role does not
            exists, it is created.
        """
        roles = ['Teacher', 'Student']
        for role in roles:
            Group.objects.get_or_create(name=role)
        self.stdout.write(
            self.style.SUCCESS('Roles created successfully!')
        )