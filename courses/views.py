from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Course, Enrollment, Lesson, Quiz, Question, Answer, Take, TakeAnswer
from .forms import QuizSubmissionForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# @login_required
# def course_list_view(request):
#     """
#     Display a list of all available courses and indicates whether
#     the logged-in user is already enrolled.
#     """
#     user_enrollments = Enrollment.objects.filter(
#         student_id=request.user
#     ).values_list('course_id', flat=True)

#     courses = Course.objects.all()

#     return render(
#         request,
#         'courses/course_list.html',
#         {
#             'courses': courses,
#             'user_enrollments': set(user_enrollments)
#         }
#     )

@login_required
def course_list_view(request):
    query = request.GET.get('q', '')
    enrolled_only = request.GET.get('enrolled_only')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(title__icontains=query)

    enrolled_courses = Enrollment.objects.filter(
        student=request.user
    ).values_list('course_id', flat=True)

    if enrolled_only == "1":
        courses = courses.filter(id__in=enrolled_courses)

    # enrollment status of user in courses
    for course in courses:
        course.is_enrolled = course.id in enrolled_courses

    return render(request, 'courses/course_list.html', {
        'courses': courses,
    })

def course_suggestions(request):
    query = request.GET.get('q', '')

    # Filter course titles by the query
    courses = Course.objects.filter(title__icontains=query)[:5]

    # Create a list of results.
    data = []
    for course in courses:
        data.append({
            'id': course.id,
            'title': course.title,
        })
    return JsonResponse(data, safe=False)

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
                messages.warning(request, "You are already enrolled in the course.")
                return redirect('course_list')

            # Enroll the user in the course (explicitly setting enrolled_at)
            Enrollment.objects.create(
                course=course,
                student=request.user,
            )
            messages.success(request, "Enrollment successful.")
            return redirect('course_lesson', course_id=course.id)
        else:
            messages.error(request, "Enrollment failed. Incorrect password.")
            return redirect('course_list')
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

@login_required
def quiz_view(request, quiz_id):
    # Fetch the quiz
    quiz = get_object_or_404(Quiz, id=quiz_id, published=True)

    # Handle form submission
    if request.method == "POST":
        form = QuizSubmissionForm(requset.POST, quiz=quiz)
        if form.is_valid():
            # Create a Take instance
            take = Take.objects.create(
                user=request.user,
                quiz=quiz,
                create_at=now()
            )

            # Save each answer
            for question, answer_id in form.cleaned_data.items():
                if answer_id:
                    answer = Answer.objects.get(id=answer_id)
                    TakeAnswer.objects.create(take=take, answer=answer)

            return redirect('quiz_result', take_id=take.id)
    else:
        form = QuizSubmissionForm(quiz=quiz)

    return render(request, 'courses/quiz/quiz_page.html', {
        'quiz': quiz,
        'form': form
    })

@login_required
def quiz_result(request, take_id):
    take = get_object_or_404(Take, id=take_id, user=request.user)

    return render(request, 'courses/quiz/quiz_result.html', {
        'take': take,
    })