# profile/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    """
    View for displaying the user's profile without the edit form.
    """
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    return render(request, 'profile/profile.html', context)

@login_required
def profile_edit_view(request):
    """
    View for editing the user's profile.
    """
    profile = Profile.objects.get(user=request.user)
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  

    context = {'form': form, 'profile': profile}
    return render(request, 'profile/edit_profile.html', context)
