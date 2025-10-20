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

class Club(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='clubs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    club_admin = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_clubs')

    def __str__(self):
        return self.name