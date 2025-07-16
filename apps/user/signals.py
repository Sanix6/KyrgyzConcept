from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(
            user=instance,
            name=instance.first_name,
            email=instance.email
        )