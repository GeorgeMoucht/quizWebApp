from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    The Profile model extends the User model to provide additional 
    fields such as bio and avatar for users. It establishes a 
    one-to-one relationship with the built-in User model.
    
    Attributes:
        user (OneToOneField): A link to the User model, creating 
            a one-to-one relationship.
        bio (TextField): A field to store a short biography 
            for the user.
        avatar (ImageField): A field to store the user's avatar image.
    
    Methods:
        __str__(self): Returns a string representation of the profile.
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(default='profiles_pics/default_pic.jpg', upload_to='profile_pics',null=True)
    
   
    def __str__(self):
        """
        Returns a string representation of the Profile object.
        
        The string returned will indicate which user the profile
        belongs to.

        Returns:
            str: A string representation of the profile, e.g. 
            "Profile of <username>"
        """

        return f"Profile of {self.user.username}"
    
    def get_avatar_url(self):
        """
        Returns the URL of the avatar.
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return f"{settings.MEDIA_URL}profiles_pics/default_pic.jpg"