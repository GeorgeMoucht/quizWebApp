from django.apps import AppConfig

class CoreConfig(AppConfig):
    """
    Configuration class for the 'core' application.

    This class sets the default auto field for models in the
    applicaiton and ensures that any necessary signals are connected
    when the application is ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Executes when the application is ready.
        """
        from .signals import assign_teacher_permissions
        # assign_teacher_permissions()
        from django.contrib.auth.models import Group, Permission
