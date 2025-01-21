from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Course, Enrollment, Lesson
from django.contrib.auth.decorators import login_required



@login_required
def course_list_view(request):
    """
    Display a list of all available courses and indicates whether
    the logged-in user is already enrolled.
    """
    user_enrollments = Enrollment.objects.filter(
        student_id=request.user
    ).values_list('course_id', flat=True)

    courses = Course.objects.all()

    return render(
        request,
        'courses/course_list.html',
        {
            'courses': courses,
            'user_enrollments': set(user_enrollments)
        }
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
                course_id=course,
                student_id=request.user,
            )
            return HttpResponse("Enrollment successful")
        else:
            return HttpResponse("Enrollment failed. Incorrect password.", status=403)
    return redirect('course_list')

@login_required
def enrolled_courses_view(request):
    """
    View για να εμφανίζει τα μαθήματα στα οποία είναι εγγεγραμμένος ο χρήστης.
    """
    enrolled_courses = request.user.courses_enrolled.all()  # Παίρνουμε τα μαθήματα μέσω του related_name
    return render(request, 'courses/enrolled_courses.html', {'enrolled_courses': enrolled_courses})

@login_required
def course_lessons_view(request, course_id):
    """
    View για να εμφανίζει τα lessons ενός μαθήματος στο οποίο είναι εγγεγραμμένος ο χρήστης.
    """
    # course = get_object_or_404(request.user.courses_enrolled, id=course_id)  # Ελέγχουμε ότι ο χρήστης είναι εγγεγραμμένος
    # lessons = course.lessons.all()  # Παίρνουμε τα lessons του μαθήματος
    # quizzes = course.quizzes.all()

    # return render(
    #     request,
    #     'courses/course_lessons.html',
    #     {
    #         'course': course,
    #         'lessons': lessons,
    #         'quizzes': quizzes
    #     }
    # )
    course = get_object_or_404(Course, id=course_id)
    lesson_id = request.GET.get('lesson')
    lesson = None
    if lesson_id:
        lesson = course.lessons.filter(id=lesson_id).first()
    else:
        lesson = course.lessons.first()

    quizzes = course.quizzes.all()

    return render(request, 'courses/course_lessons.html', {
        'course': course,
        'lesson': lesson,
        'quizzes': quizzes
    })
