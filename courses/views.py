from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required


def course_list_view(request):
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

@login_required
def enroll_course_view(request, course_id):
    """
    Handles enrolling a user into a course.

    Args:
        request (HttpRequest): The request object.
        course_id (int): The ID of the course to enroll in.

    Returns:
        HttpResponse: Redirects to the course list after enrolling.
    """
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        entered_password = request.POST.get('password', '')

        # Check if the password is correct
        if course.password and course.password == entered_password:
            # Check if the user is already enrolled
            if Enrollment.objects.filter(course=course, student=request.user).exists():
                return HttpResponse("You are already enrolled in this course.", status=400)

            # Enroll the user in the course (explicitly setting enrolled_at)
            Enrollment.objects.create(
                course=course,
                student=request.user,
            )
            return HttpResponse("Enrollment successful")
        else:
            return HttpResponse("Enrollment failed. Incorrect password.", status=403)
    return redirect('course_list')