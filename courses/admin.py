from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin inteface for managing the Course model.

    This class customize the Django admin interface for the 'Course'
    model by specifying which fields should be displayed in the
    list view. In this case the course title, the teacher associated
    with the course, and the creation date.

    Attributes:
        list_display (tuple): Specifies the fields to display in the
                            list view of the course model in Django
                            admin panel.
    """
    list_display = ('title', 'teacher', 'created_at')
