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


class Member(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')
    full_name = models.CharField(max_length=120)
    profile_pic = models.ImageField(upload_to='members/', blank=True, null=True)
    ROLE_CHOICES = [
        ('Convenor', 'Convenor'),
        ('Co-Convenor', 'Co-Convenor'),
        ('Advisor', 'Advisor'),
        ('Co-Advisor', 'Co-Advisor'),
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Selector', 'Selector'),
        ('General Secretary', 'General Secretary'),
        ('Chief Executive', 'Chief Executive'),
        ('Executive', 'Executive'),
        ('Junior Executive', 'Junior Executive'),
        ('Treasurer', 'Treasurer'),
        ('Coordinator', 'Coordinator'),
        ('Event Coordinator', 'Event Coordinator'),
        ('Media & Publications', 'Media & Publications'),
        ('Creative Graphics Executive', 'Creative Graphics Executive'),
        ('Seeker', 'Seeker'),
        ('Controller', 'Controller'),
        ('Manager', 'Manager'),
        ('Infrastructure Manager', 'Infrastructure Manager'),
        ('Department Representative', 'Department Representative'),
        ('Member', 'Member'),

    ]
    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='Member')
    email = models.EmailField()

    def __str__(self):
        return f"{self.full_name} — {self.club.name}"

