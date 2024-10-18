from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'regular'),
        (2, 'admin'),
    )
    
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

    def is_admin_user(self):
        return self.user_type == 2

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)