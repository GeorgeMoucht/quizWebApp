#profiles/urls.py
from django.urls import path
from .views import profile_view,profile_edit_view

urlpatterns = [
    path('', profile_view, name='profile_view'),
    path('edit/', profile_edit_view, name='profile_edit_view'),
]
