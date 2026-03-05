from rest_framework import serializers
from .models import (
    EducationLevel, Grade, Subject, Cluster, ClusterSubjectRequirement,
    Career, AcademicRecord, CareerPrediction
)


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'name', 'code', 'description', 'order']


class GradeSerializer(serializers.ModelSerializer):
    education_level_name = serializers.CharField(source='education_level.name', read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'name', 'code', 'education_level', 'education_level_name', 'order', 'age_range']


class SubjectSerializer(serializers.ModelSerializer):
    education_levels = EducationLevelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'education_levels', 'is_core']


class ClusterSubjectRequirementSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = ClusterSubjectRequirement
        fields = ['id', 'subject', 'subject_name', 'minimum_grade', 'is_mandatory']


class ClusterSerializer(serializers.ModelSerializer):
    requirements = ClusterSubjectRequirementSerializer(source='clustersubjectrequirement_set', many=True, read_only=True)
    
    class Meta:
        model = Cluster
        fields = ['id', 'name', 'code', 'description', 'requirements']


class CareerSerializer(serializers.ModelSerializer):
    cluster_name = serializers.CharField(source='cluster.name', read_only=True)
    
    class Meta:
        model = Career
        fields = [
            'id', 'name', 'description', 'cluster', 'cluster_name',
            'salary_range', 'job_outlook', 'required_qualifications',
            'skills_needed', 'related_courses', 'industry', 'is_active',
            'created_at', 'updated_at'
        ]


class AcademicRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    grade_level_name = serializers.CharField(source='grade_level.name', read_only=True)
    
    class Meta:
        model = AcademicRecord
        fields = [
            'id', 'student', 'student_name', 'subject', 'subject_name',
            'grade_level', 'grade_level_name', 'year', 'term', 'score',
            'grade', 'remarks', 'created_at', 'updated_at'
        ]


class CareerPredictionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    career_name = serializers.CharField(source='career.name', read_only=True)
    
    class Meta:
        model = CareerPrediction
        fields = [
            'id', 'student', 'student_name', 'career', 'career_name',
            'predicted_success_rate', 'gap_analysis', 'recommended_resources',
            'prediction_date'
        ]
