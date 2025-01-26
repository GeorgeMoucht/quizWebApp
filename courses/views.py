from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Course, Enrollment, Lesson, Quiz, Question, Answer, Take, TakeAnswer
from .forms import QuizSubmissionForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from collections import defaultdict


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
def quiz_question(request, quiz_id, question_number):
    # Fetch the quiz and ensure it's published
    quiz = get_object_or_404(Quiz, id=quiz_id, published=True)

    # Fetch all questions for this quiz, ordered by their creation
    questions = quiz.questions.all().order_by('id')

    # Ensure the question number is valid
    if question_number < 1 or question_number > questions.count():
        return redirect('quiz_page', quiz_id=quiz.id)

    # Get the current question
    question = questions[question_number - 1]

    # Pre-calculate answers for True/False questions
    true_answer = None
    false_answer = None
    if question.type == Question.TRUE_FALSE:
        true_answer = question.answers.filter(is_correct=True).first()
        false_answer = question.answers.filter(is_correct=False).first()

    # Handle form submission
    if request.method == 'POST':
        user_answers = request.POST.getlist('answer')  # For multiple-choice questions
        take, _ = Take.objects.get_or_create(user=request.user, quiz=quiz)

        if question.type == Question.SHORT_ANSWER:
            user_answer = request.POST.get('answer')
            if user_answer:
                TakeAnswer.objects.update_or_create(
                    take=take,
                    answer=None,
                    content=user_answer,
                    defaults={'created_at': now()}
                )
        else:
            for user_answer in user_answers:
                answer = question.answers.filter(id=user_answer).first()
                if answer:
                    TakeAnswer.objects.update_or_create(
                        take=take,
                        answer=answer,
                        defaults={'content': answer.content, 'created_at': now()}
                    )

        if question_number < questions.count():
            return redirect('quiz_question', quiz_id=quiz.id, question_number=question_number + 1)
        else:
            return redirect('quiz_result', take_id=take.id)

    return render(request, 'quiz/quiz_question.html', {
        'quiz': quiz,
        'question': question,
        'question_number': question_number,
        'total_questions': questions.count(),
        'true_answer': true_answer,
        'false_answer': false_answer,
    })



@login_required
def redirect_to_first_question(request, quiz_id):
    """
    Redirects to the first question of the quiz.
    """
    return redirect('quiz_question', quiz_id=quiz_id, question_number=1)

@login_required
def quiz_result(request, take_id):
    take = get_object_or_404(Take, id=take_id, user=request.user)
    quiz = take.quiz

    # Fetch all user answers and group them by question
    user_answers = take.take_answers.select_related('answer', 'answer__question')
    
    answers_by_question = {}
    for user_answer in user_answers:
        question = user_answer.answer.question if user_answer.answer else None
        if question:
            if question not in answers_by_question:
                answers_by_question[question] = []
            answers_by_question[question].append(user_answer)

    # Calculate the score
    total_questions = quiz.questions.count()
    total_possible_score = quiz.score
    total_earned_score = 0

    # score = correct_answers  # You can adjust scoring logic here

    for question, answers in answers_by_question.items():
        if question.type == Question.MULTIPLE_CHOICE:
            if all(answer.answer.is_correct for answer in answers):
                total_earned_score += question.score
        elif question.type == Question.TRUE_FALSE:
            if len(answers) == 1 and answers[0].answer.is_correct:
                total_earned_score += question.score
        elif question.type == Question.SHORT_ANSWER:
            total_earned_score += question.score

    # Update the Take record
    if take.score != total_earned_score:
        take.score = total_earned_score
        take.save()

    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'score': total_earned_score,
        'total_questions': total_questions,
        'total_possible_score': total_possible_score,
        'answers_by_question': answers_by_question,
    })
