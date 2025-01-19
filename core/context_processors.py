from profiles.models import Profile

def user_profile(request):
    """
    A context processor to make the authenticated user's
    Profile available globally in all templates.

    This function retrieves the Profile associated with
    the logged-in user and adds it to the template context
    under the key `user_profile`.

    Args:
        request (HttpRequest): The incoming HTTP request
                               object.
        Returns:
            dict: A dictionary containing the 
                  `user_profile` key which maps to the
                  user's Profile object if authenticated,
                  or None otherwise.
    """
    if request.user.is_authenticated:
        try:
            # Attempt to retrieve the user's Profile
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # Handle cases where the user does not have profile
            profile = None
        return {'user_profile': profile}
    # Return None if the user is not authenticated.
    return {'user_profile': None}