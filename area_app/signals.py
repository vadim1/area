from area_app.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from profile.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
