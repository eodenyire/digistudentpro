from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Strand, SubStrand, LearningResource, ResourceProgress,
    Assessment, AssessmentAttempt
)
from .serializers import (
    StrandSerializer, SubStrandSerializer, LearningResourceSerializer,
    ResourceProgressSerializer, AssessmentSerializer, AssessmentAttemptSerializer
)


class StrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Strand.objects.select_related('subject', 'grade').all()
    serializer_class = StrandSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'grade']


class SubStrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubStrand.objects.select_related('strand').all()
    serializer_class = SubStrandSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['strand']


class LearningResourceViewSet(viewsets.ModelViewSet):
    queryset = LearningResource.objects.select_related('sub_strand', 'author').filter(is_published=True)
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['resource_type', 'difficulty', 'sub_strand', 'is_featured']
    search_fields = ['title', 'description']
    lookup_field = 'slug'


class ResourceProgressViewSet(viewsets.ModelViewSet):
    queryset = ResourceProgress.objects.select_related('student__user', 'resource').all()
    serializer_class = ResourceProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'resource', 'is_completed']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        if hasattr(self.request.user, 'student_profile'):
            return self.queryset.filter(student=self.request.user.student_profile)
        return self.queryset.none()


class AssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assessment.objects.select_related('resource').prefetch_related('questions__answers').all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssessmentAttemptViewSet(viewsets.ModelViewSet):
    queryset = AssessmentAttempt.objects.select_related('student__user', 'assessment__resource').all()
    serializer_class = AssessmentAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'assessment', 'passed']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        if hasattr(self.request.user, 'student_profile'):
            return self.queryset.filter(student=self.request.user.student_profile)
        return self.queryset.none()
