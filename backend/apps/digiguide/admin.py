from django.contrib import admin
from .models import (
    EducationLevel, Grade, Subject, Cluster, ClusterSubjectRequirement,
    Career, AcademicRecord, CareerPrediction
)


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order']
    list_editable = ['order']
    search_fields = ['name', 'code']
    ordering = ['order']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'education_level', 'order', 'age_range']
    list_filter = ['education_level']
    list_editable = ['order']
    search_fields = ['name', 'code']
    ordering = ['education_level__order', 'order']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_core']
    list_filter = ['is_core', 'education_levels']
    search_fields = ['name', 'code']
    filter_horizontal = ['education_levels']


class ClusterSubjectRequirementInline(admin.TabularInline):
    model = ClusterSubjectRequirement
    extra = 1
    autocomplete_fields = ['subject']


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    inlines = [ClusterSubjectRequirementInline]


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'cluster', 'industry', 'is_active', 'created_at']
    list_filter = ['is_active', 'cluster', 'industry', 'created_at']
    search_fields = ['name', 'description', 'industry']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'description', 'cluster', 'industry')}),
        ('Career Details', {'fields': ('salary_range', 'job_outlook', 'required_qualifications', 'skills_needed', 'related_courses')}),
        ('Status', {'fields': ('is_active',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'grade_level', 'year', 'term', 'score', 'grade']
    list_filter = ['year', 'term', 'grade', 'grade_level', 'subject']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__user__email']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['student', 'subject', 'grade_level']
    
    fieldsets = (
        ('Student Information', {'fields': ('student', 'grade_level')}),
        ('Performance', {'fields': ('subject', 'year', 'term', 'score', 'grade', 'remarks')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(CareerPrediction)
class CareerPredictionAdmin(admin.ModelAdmin):
    list_display = ['student', 'career', 'predicted_success_rate', 'prediction_date']
    list_filter = ['prediction_date', 'career']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'career__name']
    readonly_fields = ['prediction_date']
    autocomplete_fields = ['student', 'career']
