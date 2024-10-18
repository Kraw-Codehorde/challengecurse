from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model that handles roles for the users.
    I made the choice of having regular users and admins as staff users,
    and leaving superusers as they are.
    TODO: change naming convention of 'regular' to 'client'
    """
    USER_TYPE_CHOICES = (
        (1, 'regular'),
        (2, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

    def is_admin_user(self):
        return self.user_type == 2

    def save(self, *args, **kwargs):
        self.is_staff = True    # mandatory for admin site.
        super().save(*args, **kwargs)