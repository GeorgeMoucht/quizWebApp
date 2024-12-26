from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Confguration class for the 'authentication' application.

    This class is responsible for setting up the application
    configuration and initializing any application-specific behavior,
    shuc ass signal registration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        """
        Method called when the application is ready.

        This is used to import and connect the signals defined in the
        'signals.py' file to ensure they are registered and
        executed when relevant events occur.
        """
        import authentication.signals #Import the signals