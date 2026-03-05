from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EducationLevelViewSet, GradeViewSet, SubjectViewSet,
    ClusterViewSet, CareerViewSet, AcademicRecordViewSet,
    CareerPredictionViewSet
)

router = DefaultRouter()
router.register('education-levels', EducationLevelViewSet, basename='education-level')
router.register('grades', GradeViewSet, basename='grade')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('clusters', ClusterViewSet, basename='cluster')
router.register('careers', CareerViewSet, basename='career')
router.register('academic-records', AcademicRecordViewSet, basename='academic-record')
router.register('predictions', CareerPredictionViewSet, basename='prediction')

urlpatterns = [
    path('', include(router.urls)),
]
