from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration for the 'profiles' app.

    This class is used bt Django to configure the 'profiles' app.
    It ensures that the app's settings are loaded and that any 
    necessary startup procedures for this app are executed.

    Attributes:
        default_auto_field (str): The default field typo for 
                auto-generated primary keys.
        name (str): The full Python path to the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
