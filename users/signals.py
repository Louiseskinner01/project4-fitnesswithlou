from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    # Create a profile for new users
    if created:
        UserProfile.objects.create(user=instance)

    # Save existing profile
    instance.userprofile.save()