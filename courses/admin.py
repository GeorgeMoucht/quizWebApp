from django.contrib import admin
from .models import Course, Enrollment, Lesson
from django.urls import reverse
from django.utils.html import format_html

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('student_id', 'course_id', 'enrolled_at')
    can_delete = True

    def get_queryset(self, request):
        """
        Restrict the displayed enrollments to the teacher's courses.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course_id__teacher_id=request.user)

    def has_add_permission(self, request, obj=None):
        """Prevent adding enrollments directly from this inline"""
        return False


class LessonInline(admin.TabularInline):
    """
    Inline display of lessons associated with a course.
    """
    model = Lesson
    extra = 0  # No extra empty forms
    readonly_fields = ('lesson_title', 'created_at')  # Show only non-editable fields
    can_delete = True  # Allow deleting lessons

    def lesson_title(self, obj):
        """
        Custom method to render the lesson title as a clickable link to its edit page.
        """
        # Get the URL to the lesson change page
        url = reverse('admin:courses_lesson_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.title)
    
    lesson_title.short_description = 'Lesson Title'  # Optional: Customize column header
    exclude = ('title', 'description', 'attachment')  # Hide these fields from display

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Course model.
    """
    list_display = ('title', 'get_teacher', 'created_at')
    # inlines = [EnrollmentInline, LessonInline]
    inlines = [EnrollmentInline, LessonInline]

    def get_teacher(self, obj):
        """
        Display the teacher's username.
        """
        return obj.teacher_id.username
    get_teacher.short_description = 'Teacher'

    def save_model(self, request, obj, form, change):
        """
        Set the teacher field to the current user for new courses.
        """
        if not obj.pk and not request.user.is_superuser:
            obj.teacher_id = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """
        Override the form to make the teacher field read-only for non-superusers.
        """
        form = super().get_form(request, obj, **kwargs)
        # For non-superusers, auto-fill and disable the taecher field
        if not request.user.is_superuser:
            form.base_fields['teacher_id'].initial = request.user
            form.base_fields['teacher_id'].disabled = True
        return form
    
    def get_queryset(self, request):
        """
        Restrict courses shown to those taught by the logged-in teacher.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher_id=request.user)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Lesson model.
    """
    list_display = ('title', 'course_id', 'created_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the Enrollment model.
    """
    list_display = ('get_student', 'get_course', 'enrolled_at')  # Fields to display in list view
    list_filter = ('course_id',)  # Use a tuple for filtering
    search_fields = ('student_id__username', 'course_id__title')  # Updated field names
    ordering = ('-enrolled_at',)  # Use a tuple for ordering (descending by enrollment date)

    def get_student(self, obj):
        """
        Display the enrolled student's username.
        """
        return obj.student_id.username
    get_student.short_description = 'Student'

    def get_course(self, obj):
        """
        Display the course title.
        """
        return obj.course_id.title
    get_course.short_description = 'Course'

    def get_queryset(self, request):
        """
        Restrict the displayed enrollments based on the logged-in user's role.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course_id__teacher_id=request.user)
    
    def has_view_permission(self, request, obj=None):
        """
        Allow teachers to view enrollments if they're associated
        with their courses.
        """
        if request.user.is_superuser:
            return True
        if obj and obj.course_id.teacher_id == request.user:
            return True
        return False
    
    def has_delete_permission(self, request, obj =None):
        """
        Allow teachers to delete enrollments for their courses.
        """
        if request.user.is_superuser:
            return True
        # Ensure the teacher has permission to delete enrollments in their course
        return obj and obj.course_id.teacher_id == request.user

    def has_add_permission(self, request):
        """Disable adding enrollments directly from the admin."""
        return False
