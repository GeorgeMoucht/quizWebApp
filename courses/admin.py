from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Course model.
    """
    list_display = ('title', 'teacher', 'created_at')

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to automatically set the teacher field to the current user.
        """
        # If this is a new course and the teacher is not set, set the teacher to the current logged-in user.
        if not obj.pk:  # This means the course is not yet saved to the DB
            if not request.user.is_superuser:
                obj.teacher = request.user  # Assign the logged-in user as the teacher
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """
        Override the form to make the teacher field read-only for non-superusers.
        """
        form = super().get_form(request, obj, **kwargs)

        # For non-superusers, auto-fill and disable the taecher field
        if not request.user.is_superuser:
            form.base_fields['teacher'].initial = request.user
            form.base_fields['teacher'].disabled = True
        return form
