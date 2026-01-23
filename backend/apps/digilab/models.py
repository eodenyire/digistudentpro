from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


class Strand(models.Model):
    """
    Learning strands for subjects
    e.g., "Mixtures and Elements" for Integrated Science
    """
    subject = models.ForeignKey('digiguide.Subject', on_delete=models.CASCADE, related_name='strands')
    grade = models.ForeignKey('digiguide.Grade', on_delete=models.CASCADE, related_name='strands')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['subject', 'grade', 'order']
        unique_together = ['subject', 'grade', 'code']
        verbose_name = 'Strand'
        verbose_name_plural = 'Strands'
    
    def __str__(self):
        return f"{self.subject.name} - {self.grade.name} - {self.name}"


class SubStrand(models.Model):
    """
    Sub-strands representing specific learning outcomes
    """
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, related_name='sub_strands')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    learning_outcome = models.TextField(help_text="Specific learning outcome description")
    order = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['strand', 'order']
        unique_together = ['strand', 'code']
        verbose_name = 'Sub-Strand'
        verbose_name_plural = 'Sub-Strands'
    
    def __str__(self):
        return f"{self.strand.name} - {self.name}"


class LearningResource(models.Model):
    """
    Learning resources (text, video, audio, PDF, assessments)
    """
    RESOURCE_TYPE_CHOICES = [
        ('text', 'Text/HTML'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('pdf', 'PDF Document'),
        ('assessment', 'Assessment/Quiz'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    sub_strand = models.ForeignKey(SubStrand, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    description = models.TextField(blank=True)
    
    # Content fields
    content = models.TextField(blank=True, help_text="HTML content for text resources")
    file = models.FileField(
        upload_to='resources/%Y/%m/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'mp4', 'mp3', 'webm', 'ogg'])]
    )
    external_url = models.URLField(blank=True, null=True, help_text="YouTube, Vimeo, etc.")
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    
    # Metadata
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration for video/audio resources"
    )
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_resources'
    )
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['sub_strand', 'order', '-created_at']
        verbose_name = 'Learning Resource'
        verbose_name_plural = 'Learning Resources'
        indexes = [
            models.Index(fields=['resource_type', 'is_published']),
            models.Index(fields=['sub_strand', 'is_published']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while LearningResource.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ResourceProgress(models.Model):
    """
    Track student progress on learning resources
    """
    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='resource_progress'
    )
    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.PositiveIntegerField(default=0)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'resource']
        ordering = ['-last_accessed']
        verbose_name = 'Resource Progress'
        verbose_name_plural = 'Resource Progress'
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.resource.title} ({self.completion_percentage}%)"


class Assessment(models.Model):
    """
    Assessments and quizzes for learning resources
    """
    resource = models.OneToOneField(
        LearningResource,
        on_delete=models.CASCADE,
        related_name='assessment',
        limit_choices_to={'resource_type': 'assessment'}
    )
    passing_score = models.PositiveIntegerField(default=70, help_text="Passing percentage")
    time_limit_minutes = models.PositiveIntegerField(null=True, blank=True)
    max_attempts = models.PositiveIntegerField(default=3)
    show_correct_answers = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'
    
    def __str__(self):
        return f"Assessment: {self.resource.title}"


class Question(models.Model):
    """
    Questions for assessments
    """
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True, help_text="Explanation for correct answer")
    
    class Meta:
        ordering = ['assessment', 'order']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
    def __str__(self):
        return f"{self.assessment.resource.title} - Q{self.order}"


class Answer(models.Model):
    """
    Answer options for questions
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['question', 'order']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
    
    def __str__(self):
        return f"{self.question} - {self.answer_text[:50]}"


class AssessmentAttempt(models.Model):
    """
    Student assessment attempts
    """
    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='assessment_attempts'
    )
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=False)
    answers = models.JSONField(help_text="Student answers and results")
    time_taken_minutes = models.PositiveIntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Assessment Attempt'
        verbose_name_plural = 'Assessment Attempts'
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assessment.resource.title} ({self.score}%)"
