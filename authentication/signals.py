from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from profiles.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a Profile instance whenever
    a new User is created.

    Args:
        sender (Model): The model class that triggered the signal.
        instance (User): The specific instance of the model that
                         triggered the signal.
        created (bool): A boolean indicating whether a new record
                        was created.
        **kwargs: Additional keyword argument provided by the signal.

    Behavior:
        If a new User instance is created, the signal creates a
        corresponding Profile instance.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to automatically save the related Profile instance
    whenever a User instance is saved.

    Args:
        sender (Model): The model class that triggered the signal
        instance (User): The specific instance of the model that
                         triggered the signal.
        **kwargs: Additional keyword arguments provided by the signal.
    """
    instance.profile.save()