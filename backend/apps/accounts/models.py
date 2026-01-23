from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    Supports multiple user roles for the DigiStudentPro platform
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('parent', 'Parent/Guardian'),
        ('teacher', 'Teacher'),
        ('admin', 'Administrator'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class StudentProfile(models.Model):
    """
    Student Profile - The "Golden Record"
    Comprehensive tracking of student information
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    current_grade = models.ForeignKey('digiguide.Grade', on_delete=models.SET_NULL, null=True, blank=True)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, help_text="Comma-separated interests")
    career_aspirations = models.TextField(blank=True)
    has_parental_consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"Student: {self.user.get_full_name()}"


class MentorProfile(models.Model):
    """
    Mentor Profile for verified mentors
    """
    VERIFICATION_STATUS = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    profession = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(help_text="Brief biography and expertise")
    areas_of_expertise = models.TextField(help_text="Comma-separated areas")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verification_document = models.FileField(upload_to='mentor_verifications/', blank=True, null=True)
    badge_earned = models.BooleanField(default=False)
    years_of_experience = models.PositiveIntegerField(default=0)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mentor Profile'
        verbose_name_plural = 'Mentor Profiles'
    
    def __str__(self):
        return f"Mentor: {self.user.get_full_name()} - {self.profession}"


class ParentGuardian(models.Model):
    """
    Parent/Guardian information linked to students
    """
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Legal Guardian'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    students = models.ManyToManyField(StudentProfile, related_name='parents')
    phone_number = models.CharField(max_length=15)
    alternative_phone = models.CharField(max_length=15, blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True, help_text="National ID or Passport")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Parent/Guardian'
        verbose_name_plural = 'Parents/Guardians'
    
    def __str__(self):
        return f'{self.get_relationship_display()} - {self.user.get_full_name()}'
