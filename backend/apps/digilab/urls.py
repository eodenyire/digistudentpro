from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StrandViewSet, SubStrandViewSet, LearningResourceViewSet,
    ResourceProgressViewSet, AssessmentViewSet, AssessmentAttemptViewSet
)

router = DefaultRouter()
router.register('strands', StrandViewSet, basename='strand')
router.register('sub-strands', SubStrandViewSet, basename='sub-strand')
router.register('resources', LearningResourceViewSet, basename='resource')
router.register('progress', ResourceProgressViewSet, basename='progress')
router.register('assessments', AssessmentViewSet, basename='assessment')
router.register('attempts', AssessmentAttemptViewSet, basename='attempt')

urlpatterns = [
    path('', include(router.urls)),
]
