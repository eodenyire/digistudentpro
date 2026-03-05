from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SquadViewSet, SquadMembershipViewSet, MessageViewSet, DirectMessageViewSet, MessageReportViewSet

router = DefaultRouter()
router.register('squads', SquadViewSet, basename='squad')
router.register('memberships', SquadMembershipViewSet, basename='membership')
router.register('messages', MessageViewSet, basename='message')
router.register('direct-messages', DirectMessageViewSet, basename='direct-message')
router.register('reports', MessageReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
