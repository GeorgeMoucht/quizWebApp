from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    # Link Profile to the User model with 
    # One-to-One relationship
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
        )
    
    def __str__(self):
        return f"Profile of {self.user.username}"