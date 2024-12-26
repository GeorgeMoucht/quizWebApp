from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
@login_required
def profile_view(request):
    """
    View for displaying the user's profile.

    This view is only accessible to authenticated users. It retrieves
    the profile related to the logged-in user and renders it on a
    profile page.

    The user is required to be logged in to view this page. If the user
    is not logged in, they will be redirected to the login page.

    Args:
        request (HttpRequest): The request object containing metadata
            about the current request (e.g., user, session).

    Returns:
        HttpResponse: The rendered profile page with the user's
                profile data.
    
    Raises:
        Profile.DoesNotExist: If the user does not have an associated 
                profile, an exception will be raised.
    """
    # profile = request.user.profile
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})