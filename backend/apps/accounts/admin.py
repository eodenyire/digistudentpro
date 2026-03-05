from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, StudentProfile, MentorProfile, ParentGuardian


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model"""
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_verified', 'is_staff']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin interface for Student Profile"""
    list_display = ['user', 'student_id', 'gender', 'current_grade', 'school_name', 'county', 'has_parental_consent']
    list_filter = ['gender', 'current_grade', 'county', 'has_parental_consent', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'student_id', 'school_name']
    raw_id_fields = ['user', 'current_grade']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {'fields': ('user', 'student_id')}),
        ('Personal Details', {'fields': ('gender', 'current_grade', 'school_name', 'county')}),
        ('Interests & Aspirations', {'fields': ('interests', 'career_aspirations')}),
        ('Consent', {'fields': ('has_parental_consent', 'consent_date')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    """Admin interface for Mentor Profile"""
    list_display = ['user', 'profession', 'verification_status', 'badge_earned', 'years_of_experience', 'verified_at']
    list_filter = ['verification_status', 'badge_earned', 'created_at', 'verified_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'profession', 'organization']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at', 'verified_at']
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Professional Details', {'fields': ('profession', 'organization', 'bio', 'areas_of_expertise', 'years_of_experience', 'linkedin_url')}),
        ('Verification', {'fields': ('verification_status', 'verification_document', 'badge_earned', 'verified_at')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
    
    actions = ['verify_mentors', 'reject_mentors']
    
    def verify_mentors(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(verification_status='verified', verified_at=timezone.now())
        self.message_user(request, f'{count} mentor(s) verified successfully.')
    verify_mentors.short_description = 'Verify selected mentors'
    
    def reject_mentors(self, request, queryset):
        count = queryset.update(verification_status='rejected')
        self.message_user(request, f'{count} mentor(s) rejected.')
    reject_mentors.short_description = 'Reject selected mentors'


@admin.register(ParentGuardian)
class ParentGuardianAdmin(admin.ModelAdmin):
    """Admin interface for Parent/Guardian"""
    list_display = ['user', 'relationship', 'phone_number', 'alternative_phone']
    list_filter = ['relationship', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone_number', 'id_number']
    raw_id_fields = ['user']
    filter_horizontal = ['students']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {'fields': ('user', 'relationship')}),
        ('Contact Details', {'fields': ('phone_number', 'alternative_phone', 'id_number')}),
        ('Linked Students', {'fields': ('students',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
