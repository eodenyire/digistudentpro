from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, StudentProfileViewSet,
    MentorProfileViewSet, ParentGuardianViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('students', StudentProfileViewSet, basename='student')
router.register('mentors', MentorProfileViewSet, basename='mentor')
router.register('parents', ParentGuardianViewSet, basename='parent')

urlpatterns = [
    path('', include(router.urls)),
]
