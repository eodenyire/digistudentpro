from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Squad, SquadMembership, Message, DirectMessage, MessageReport
from .serializers import SquadSerializer, SquadMembershipSerializer, MessageSerializer, DirectMessageSerializer, MessageReportSerializer


class SquadViewSet(viewsets.ModelViewSet):
    queryset = Squad.objects.all()
    serializer_class = SquadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_public', 'topic']


class SquadMembershipViewSet(viewsets.ModelViewSet):
    queryset = SquadMembership.objects.select_related('squad', 'user').all()
    serializer_class = SquadMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['squad', 'user', 'role']


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('squad', 'sender').all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['squad', 'sender', 'is_flagged']


class DirectMessageViewSet(viewsets.ModelViewSet):
    queryset = DirectMessage.objects.select_related('sender', 'recipient').all()
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'recipient', 'is_read']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(models.Q(sender=self.request.user) | models.Q(recipient=self.request.user))


class MessageReportViewSet(viewsets.ModelViewSet):
    queryset = MessageReport.objects.select_related('reported_by').all()
    serializer_class = MessageReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report_type', 'status']

