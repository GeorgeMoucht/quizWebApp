from django.urls import path
from . import views

urlpatterns = [
    path('courses/',views.course_list_view,name='course_list'),
    path('courses/enroll/<int:course_id>/',views.enroll_course_view,name='enroll_course'),
    path('courses/enrolled/', views.enrolled_courses_view, name='enrolled_courses'),
    path('courses/enrolled/lessons/<int:course_id>/', views.course_lessons_view, name='course_lessons'),
    path('courses/quiz/<int:quiz_id>/', views.quiz_view, name='quiz_page'),
    path('courses/quiz/result/<int:take_id>/', views.quiz_result, name='quiz_result'),
]