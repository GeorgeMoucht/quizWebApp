from django.urls import path
from . import views

urlpatterns = [
    path('courses/',views.course_list_view,name='course_list'),
    path('course/enroll/<int:course_id>/',views.enroll_course_view,name='enroll_course'),
    path('courses/enrolled/', views.enrolled_courses_view, name='enrolled_courses'),
    path('course/lesson/<int:course_id>/', views.course_lessons_view, name='course_lesson'),
    path('courses/suggestions/', views.course_suggestions, name='course_suggestions'),
    path('courses/teachers', views.teachers_view, name="teachers"),

    path('quiz/<int:quiz_id>/', views.redirect_to_first_question, name='quiz_page'),
    path('quiz/<int:quiz_id>/question/<int:question_number>/', views.quiz_question, name='quiz_question'),
    path('quiz/result/<int:take_id>/', views.quiz_result, name="quiz_result"),
]