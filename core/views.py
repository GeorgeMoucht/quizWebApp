from django.http import HttpResponse
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
#from django.template.loader import get_template
from django.db.models import Count
from courses.models import Course  


def homepage_view(request):
    """
    View function that renders the homepage template.
    """
    try:
        popular_courses = Course.objects.annotate(num_enrollments=Count('enrollments')).order_by('-num_enrollments')[:3]
        return render(request, 'core/homepage.html', {'popular_courses': popular_courses})
    except TemplateDoesNotExist:
        return HttpResponse(
            "Template not found",
            status=404
        )
    
from django.shortcuts import render
from django.contrib.auth.models import User, Group

def teachers_view(request):
    """
    View for displaying the list of teachers.

    This view fetches all users that belong to the 'teachers' group
    and renders them in the 'teachers.html' template.
    """
    # Ανάκτηση του group των teachers
    teachers_group = Group.objects.get(name="Teacher")
    teachers = teachers_group.user_set.all()  # Παίρνουμε τους χρήστες του group

    return render(request, 'core/teachers.html', {'teachers': teachers})
