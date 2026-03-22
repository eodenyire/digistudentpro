from rest_framework import serializers
from .models import (
    Strand, SubStrand, LearningResource, ResourceProgress,
    Assessment, Question, Answer, AssessmentAttempt
)


class StrandSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    
    class Meta:
        model = Strand
        fields = ['id', 'subject', 'subject_name', 'grade', 'grade_name', 'name', 'code', 'description', 'order', 'created_at', 'updated_at']


class SubStrandSerializer(serializers.ModelSerializer):
    strand_name = serializers.CharField(source='strand.name', read_only=True)
    
    class Meta:
        model = SubStrand
        fields = ['id', 'strand', 'strand_name', 'name', 'code', 'learning_outcome', 'order', 'created_at', 'updated_at']


class LearningResourceSerializer(serializers.ModelSerializer):
    sub_strand_name = serializers.CharField(source='sub_strand.name', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = LearningResource
        fields = [
            'id', 'sub_strand', 'sub_strand_name', 'title', 'slug', 'resource_type',
            'difficulty', 'description', 'content', 'file', 'external_url', 'thumbnail',
            'duration_minutes', 'author', 'author_name', 'is_published', 'is_featured',
            'views_count', 'order', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'views_count', 'created_at', 'updated_at']


class ResourceProgressSerializer(serializers.ModelSerializer):
    resource_title = serializers.CharField(source='resource.title', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    
    class Meta:
        model = ResourceProgress
        fields = [
            'id', 'student', 'student_name', 'resource', 'resource_title',
            'is_completed', 'completion_percentage', 'time_spent_minutes',
            'last_accessed', 'completed_at', 'created_at'
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'explanation', 'answers']


class AssessmentSerializer(serializers.ModelSerializer):
    resource_title = serializers.CharField(source='resource.title', read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'resource', 'resource_title', 'passing_score', 'time_limit_minutes',
            'max_attempts', 'show_correct_answers', 'questions'
        ]


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    assessment_title = serializers.CharField(source='assessment.resource.title', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    
    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'student', 'student_name', 'assessment', 'assessment_title',
            'score', 'passed', 'answers', 'time_taken_minutes',
            'started_at', 'completed_at'
        ]
