from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import StudentProfile, MentorProfile, ParentGuardian
from .serializers import (
    UserSerializer, StudentProfileSerializer,
    MentorProfileSerializer, ParentGuardianSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User model - Read only
    User creation handled by Djoser
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Student Profile management"""
    queryset = StudentProfile.objects.select_related('user', 'current_grade').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter to show only own profile or all for admin"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's student profile"""
        try:
            profile = StudentProfile.objects.select_related(
                'user', 'current_grade'
            ).get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response(
                {'detail': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class MentorProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Mentor Profile management"""
    queryset = MentorProfile.objects.select_related('user').all()
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Show only verified mentors to non-staff, all to staff"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(verification_status='verified')
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's mentor profile"""
        try:
            profile = MentorProfile.objects.select_related('user').get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except MentorProfile.DoesNotExist:
            return Response(
                {'detail': 'Mentor profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ParentGuardianViewSet(viewsets.ModelViewSet):
    """ViewSet for Parent/Guardian management"""
    queryset = ParentGuardian.objects.select_related('user').prefetch_related('students').all()
    serializer_class = ParentGuardianSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter to show only own profile or all for admin"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)
