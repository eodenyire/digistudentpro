from django.contrib import admin
from .models import (
    Strand, SubStrand, LearningResource, ResourceProgress,
    Assessment, Question, Answer, AssessmentAttempt
)


@admin.register(Strand)
class StrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'grade', 'code', 'order']
    list_filter = ['subject', 'grade']
    search_fields = ['name', 'code']
    list_editable = ['order']


@admin.register(SubStrand)
class SubStrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'strand', 'code', 'order']
    list_filter = ['strand__subject', 'strand__grade']
    search_fields = ['name', 'code']
    list_editable = ['order']


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'difficulty', 'sub_strand', 'is_published', 'is_featured', 'views_count']
    list_filter = ['resource_type', 'difficulty', 'is_published', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    

@admin.register(ResourceProgress)
class ResourceProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'resource', 'completion_percentage', 'is_completed', 'last_accessed']
    list_filter = ['is_completed', 'last_accessed']
    search_fields = ['student__user__email', 'resource__title']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'question_type', 'points', 'order']
    list_filter = ['question_type']
    inlines = [AnswerInline]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['resource', 'passing_score', 'time_limit_minutes', 'max_attempts']


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'assessment', 'score', 'passed', 'started_at', 'completed_at']
    list_filter = ['passed', 'started_at']
    search_fields = ['student__user__email']
