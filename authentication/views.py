# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

# Register view
def register_view(request):
    """
    Handle user registration

    If the request method is POST and the form is valid, a new user
    is created, a success message is displayed, and user is
    redirected to the login page. Otherwise, the registration form
    is rendered.

    Args:
        requet (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: The rendered registration page or a redirect
                      to the login page.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account created for {username}!'
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(
        request,
        'authentication/register.html',
        {'form': form}
    )

# Login view
def login_view(request):
    """
    Handle user login.

    If the request method is POST and valid credentials are provided,
    the user is authenticated and logged in, and redirected to
    homepage. Otherwise, an error message is displayed, and the
    login form is rendered again.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or redirect to the
                      homepage.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(
                request,
                'Invalid username or password.'
            )
    return render(request, 'authentication/login.html')

# Logout view
def logout_view(request):
    """
    Handle user logout.

    Logs the user out and redirects them to the homepage.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the homepage.
    """
    logout(request)
    return redirect('homepage')