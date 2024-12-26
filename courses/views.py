from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import Course
from core.utils import is_teacher

def course_list_view(response):
    """
    Displays a list of all available courses.

    This view retrieves all courses from the database and renders
    them on the 'course_list.html' template. It allows users to see
    the titles and descriptions of the courses.

    Args: 
        request (HttpRequest): The request object that contains
                metadata about the request.
    
    Returns: The rendered 'courses/courses/course_list.html' template
            with the list of courses.
    """
    courses = Course.objects.all()
    return render(
        request,
        'courses/course_list.html',
        {'courses': courses}
    )

def create_course_view(request):
    """
    Allows a teacher to create a new course.

    This view is accessible only by users with the 'Teacher' role.
    If the user is not a teacher, an HTTP 403 (Forbidden) response
    is returned. Otherwise, the view should render a form for the
    teacher to create a new course.

    Args:
        request (HttpRequest): The request object containing metadata
                    about the request.
        
    Returns:
        HttpResponse: An HTTP response. Either a forbidden response for
        non-teachers or a form for course creation.
    """
    if not is_teacher(request.user):
        return HttpResponseForbidden("Only teacher can create courses.")
