from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        HEAD_ADMIN = 'HEAD', 'Head Admin'
        CLUB_ADMIN = 'CLUB', 'Club Admin'
        NORMAL = 'USER', 'Normal User'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.NORMAL)

    def is_head_admin(self):
        return self.role == self.Role.HEAD_ADMIN

    def is_club_admin(self):
        return self.role == self.Role.CLUB_ADMIN