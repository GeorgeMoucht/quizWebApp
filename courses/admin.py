from django.contrib import admin
from .models import Course, Enrollment

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('student', 'enrolled_at')
    can_delete = True

    def get_queryset(self, request):
        """
        Restrict the displayed enrollments to the teacher's courses.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__teacher=request.user)

    def has_add_permission(self, request, obj=None):
        """Prevent adding enrollments directly from this inline"""
        return False


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Course model.
    """
    list_display = ('title', 'teacher', 'created_at')
    inlines = [EnrollmentInline]

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
    
    def get_queryset(self, request):
        """
        Restrict courses shown to those taught by the logged-in teacher.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Enrollment model.
    """
    list_display = ('student', 'course', 'enrolled_at')  # Fields to display in list view
    list_filter = ('course',)  # Use a tuple for filtering
    search_fields = ('student__username', 'course__title')  # Enable searching
    ordering = ('-enrolled_at',)  # Use a tuple for ordering (descending by enrollment date)

    def get_queryset(self, request):
        """
        Restrict the displayed enrollments based on the logged-in user's role.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__teacher=request.user)
    
    def has_view_permission(self, request, obj=None):
        """
        Allow teachers to view enrollments if they're associated
        with their courses.
        """
        if request.user.is_superuser:
            return True
        if obj and obj.course.teacher == request.user:
            return True
        return False
    
    def has_delete_permission(self, request, obj =None):
        """
        Allow teachers to delete enrollments for their courses.
        """
        if request.user.is_superuser:
            return True
        # Ensure the teacher has permission to delete enrollments in their course
        return obj and obj.course.teacher == request.user

    def has_add_permission(self, request):
        """Disable adding enrollments directly from the admin."""
        return False
