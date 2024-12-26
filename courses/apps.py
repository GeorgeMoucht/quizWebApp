from django.apps import AppConfig


class CoursesConfig(AppConfig):
    """
    Configuration for the Courses application.

    This class configures the 'courses' app and provides necessary
    settings for the app's integration into the Django project.
    It is used to define the application name and auto-fields
    for the models.

    Attributes:
        default_auto_field (str): The default type of fields to use
                            for auto-generated primary keys. It is set
                            to 'BigAutoField'  by default.
        name (str): The name of the application. This is used by Django
                    to configure the app within the project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
