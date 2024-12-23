from django.http import HttpResponse
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template

def homepage_view(request):
    try:
        get_template('core/homepage.html')
        return render(request, 'core/homepage.html')
    except TemplateDoesNotExist:
        return HttpResponse(
            "Template not found",
            status=404
        )