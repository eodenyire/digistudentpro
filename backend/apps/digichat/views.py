from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, slug=None):
        squad = self.get_object()

        if squad.members.filter(id=request.user.id).exists():
            membership = SquadMembership.objects.get(squad=squad, user=request.user)
            data = SquadMembershipSerializer(membership).data
            return Response(data, status=status.HTTP_200_OK)

        if squad.members.count() >= squad.max_members:
            return Response(
                {'detail': 'This squad has reached the maximum number of members.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership = SquadMembership.objects.create(squad=squad, user=request.user, role='member')
        data = SquadMembershipSerializer(membership).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def leave(self, request, slug=None):
        squad = self.get_object()
        membership = SquadMembership.objects.filter(squad=squad, user=request.user).first()

        if not membership:
            return Response({'detail': 'You are not a member of this squad.'}, status=status.HTTP_404_NOT_FOUND)

        if squad.created_by_id == request.user.id:
            return Response(
                {'detail': 'Squad creator cannot leave. Transfer ownership or delete the squad.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

