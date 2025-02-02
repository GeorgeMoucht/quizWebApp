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
