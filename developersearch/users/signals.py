from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

# === anytime when we create a user, it will create profile authomaticly
#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )
#==== if profile delete, user will delete by delete signal
#@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

# conneting signals one way and another is decorators
post_save.connet(createProfile, sender=User)
post_delete.connet(deleteUser, sender=Profile)