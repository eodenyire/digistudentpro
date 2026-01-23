from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended user model with additional fields"""
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent/Guardian'),
        ('MENTOR', 'Mentor'),
        ('CONTENT_CREATOR', 'Content Creator'),
        ('ADMIN', 'Administrator'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True)
    county = models.CharField(max_length=100, blank=True)
    sub_county = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    total_points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']