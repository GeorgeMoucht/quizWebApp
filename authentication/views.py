# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
    logout(request)
    return redirect('homepage')