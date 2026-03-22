from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, MentorProfile, ParentGuardian

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'is_verified', 'date_of_birth',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone_number', 'date_of_birth'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for Student Profile"""
    user = UserSerializer(read_only=True)
    current_grade_name = serializers.CharField(source='current_grade.name', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'student_id', 'gender', 'current_grade', 
            'current_grade_name', 'school_name', 'county', 'interests',
            'career_aspirations', 'has_parental_consent', 'consent_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MentorProfileSerializer(serializers.ModelSerializer):
    """Serializer for Mentor Profile"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user', 'profession', 'organization', 'bio',
            'areas_of_expertise', 'verification_status', 'badge_earned',
            'years_of_experience', 'linkedin_url', 'created_at',
            'updated_at', 'verified_at'
        ]
        read_only_fields = [
            'id', 'verification_status', 'badge_earned',
            'created_at', 'updated_at', 'verified_at'
        ]


class ParentGuardianSerializer(serializers.ModelSerializer):
    """Serializer for Parent/Guardian"""
    user = UserSerializer(read_only=True)
    students = StudentProfileSerializer(many=True, read_only=True)
    
    class Meta:
        model = ParentGuardian
        fields = [
            'id', 'user', 'relationship', 'students', 'phone_number',
            'alternative_phone', 'id_number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
