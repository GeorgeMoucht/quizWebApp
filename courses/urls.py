from django.urls import path
from . import views

urlpatterns = [
    path(
        'courses/',
        views.course_list_view,
        name='course_list'
    ),

    path(
        'courses/enroll/<int:course_id>/',
        views.enroll_course_view,
        name='enroll_course'
    )
]