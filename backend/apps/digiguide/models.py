from django.db import models
from django.utils.translation import gettext_lazy as _


class EducationLevel(models.Model):
    """Education levels in Kenya CBC"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Education Level'
        verbose_name_plural = 'Education Levels'
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    """Grades within each education level"""
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, related_name='grades')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    order = models.PositiveIntegerField(default=0)
    age_range = models.CharField(max_length=50, blank=True, help_text="e.g., 6-7 years")
    
    class Meta:
        ordering = ['education_level__order', 'order']
        unique_together = ['education_level', 'code']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
    
    def __str__(self):
        return f"{self.education_level.name} - {self.name}"


class Subject(models.Model):
    """Subjects taught at different education levels"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    education_levels = models.ManyToManyField(EducationLevel, related_name='subjects')
    is_core = models.BooleanField(default=False, help_text="Core/compulsory subject")
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
    
    def __str__(self):
        return self.name


class Cluster(models.Model):
    """KUCCPS Clusters for university placement"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    required_subjects = models.ManyToManyField(Subject, related_name='clusters', through='ClusterSubjectRequirement')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'KUCCPS Cluster'
        verbose_name_plural = 'KUCCPS Clusters'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ClusterSubjectRequirement(models.Model):
    """Subject requirements for each cluster"""
    GRADE_CHOICES = [
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('D-', 'D-'),
        ('E', 'E'),
    ]
    
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    minimum_grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    is_mandatory = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['cluster', 'subject']
        verbose_name = 'Cluster Subject Requirement'
        verbose_name_plural = 'Cluster Subject Requirements'
    
    def __str__(self):
        return f"{self.cluster.code} - {self.subject.name} (Min: {self.minimum_grade})"


class Career(models.Model):
    """Career options mapped to clusters"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True, related_name='careers')
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., KES 50,000 - 100,000")
    job_outlook = models.TextField(blank=True, help_text="Career prospects in Kenya")
    required_qualifications = models.TextField(help_text="Educational requirements")
    skills_needed = models.TextField(blank=True)
    related_courses = models.TextField(blank=True, help_text="University/college courses")
    industry = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'
    
    def __str__(self):
        return self.name


class AcademicRecord(models.Model):
    """Student academic performance tracking"""
    GRADE_CHOICES = [
        ('A', 'A (80-100)'),
        ('A-', 'A- (75-79)'),
        ('B+', 'B+ (70-74)'),
        ('B', 'B (65-69)'),
        ('B-', 'B- (60-64)'),
        ('C+', 'C+ (55-59)'),
        ('C', 'C (50-54)'),
        ('C-', 'C- (45-49)'),
        ('D+', 'D+ (40-44)'),
        ('D', 'D (35-39)'),
        ('D-', 'D- (30-34)'),
        ('E', 'E (0-29)'),
    ]
    
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
    ]
    
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='academic_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade_level = models.ForeignKey(Grade, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(help_text="Academic year")
    term = models.PositiveSmallIntegerField(choices=TERM_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage score")
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    remarks = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-term', 'subject']
        unique_together = ['student', 'subject', 'grade_level', 'year', 'term']
        verbose_name = 'Academic Record'
        verbose_name_plural = 'Academic Records'
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} ({self.year} T{self.term}): {self.grade}"


class CareerPrediction(models.Model):
    """AI-powered career predictions based on academic performance"""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='career_predictions')
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    predicted_success_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage likelihood")
    gap_analysis = models.JSONField(help_text="Subjects needing improvement with targets")
    recommended_resources = models.JSONField(default=list, blank=True)
    prediction_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-prediction_date', '-predicted_success_rate']
        verbose_name = 'Career Prediction'
        verbose_name_plural = 'Career Predictions'
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.career.name} ({self.predicted_success_rate}%)"
