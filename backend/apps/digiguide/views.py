from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    EducationLevel, Grade, Subject, Cluster,
    Career, AcademicRecord, CareerPrediction
)
from .serializers import (
    EducationLevelSerializer, GradeSerializer, SubjectSerializer,
    ClusterSerializer, CareerSerializer, AcademicRecordSerializer,
    CareerPredictionSerializer
)


class EducationLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Education Levels - Read only"""
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
    permission_classes = [permissions.AllowAny]


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Grades - Read only"""
    queryset = Grade.objects.select_related('education_level').all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['education_level']


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Subjects - Read only"""
    queryset = Subject.objects.prefetch_related('education_levels').all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_core']
    search_fields = ['name', 'code']


class ClusterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for KUCCPS Clusters - Read only"""
    queryset = Cluster.objects.prefetch_related('clustersubjectrequirement_set__subject').all()
    serializer_class = ClusterSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Careers"""
    queryset = Career.objects.select_related('cluster').filter(is_active=True)
    serializer_class = CareerSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cluster', 'industry']
    search_fields = ['name', 'description', 'industry']


class AcademicRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for Academic Records"""
    queryset = AcademicRecord.objects.select_related(
        'student__user', 'subject', 'grade_level'
    ).all()
    serializer_class = AcademicRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'subject', 'year', 'term', 'grade_level']
    
    def get_queryset(self):
        """Filter to show only own records or all for admin"""
        if self.request.user.is_staff:
            return self.queryset
        if hasattr(self.request.user, 'student_profile'):
            return self.queryset.filter(student=self.request.user.student_profile)
        return self.queryset.none()


class CareerPredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Career Predictions - Read only"""
    queryset = CareerPrediction.objects.select_related(
        'student__user', 'career'
    ).all()
    serializer_class = CareerPredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'career']
    
    def get_queryset(self):
        """Filter to show only own predictions or all for admin"""
        if self.request.user.is_staff:
            return self.queryset
        if hasattr(self.request.user, 'student_profile'):
            return self.queryset.filter(student=self.request.user.student_profile)
        return self.queryset.none()
