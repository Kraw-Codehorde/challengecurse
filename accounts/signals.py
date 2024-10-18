from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    """
    Assigns a user to a group based on their user type.
    TODO: change naming convention of 'Regular User' to 'Client'
    """
    if created:
        if instance.user_type == 2:  # Admin
            group = Group.objects.get(name='Admin')
        else:  # Regular user
            group = Group.objects.get(name='Regular User')
        instance.groups.add(group)