from rest_framework import serializers
from .models import Squad, SquadMembership, Message, DirectMessage, MessageReport


class SquadSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Squad
        fields = ['id', 'name', 'slug', 'description', 'topic', 'created_by', 'created_by_name', 'is_public', 'max_members', 'avatar', 'member_count', 'is_member', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_member(self, obj):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.members.filter(id=request.user.id).exists()


class SquadMembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    squad_name = serializers.CharField(source='squad.name', read_only=True)
    
    class Meta:
        model = SquadMembership
        fields = ['id', 'squad', 'squad_name', 'user', 'user_name', 'role', 'joined_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'squad', 'sender', 'sender_name', 'content', 'attachment', 'is_flagged', 'flagged_reason', 'created_at', 'updated_at']


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'sender_name', 'recipient', 'recipient_name', 'content', 'attachment', 'is_read', 'read_at', 'is_flagged', 'created_at']


class MessageReportSerializer(serializers.ModelSerializer):
    reported_by_name = serializers.CharField(source='reported_by.get_full_name', read_only=True)
    
    class Meta:
        model = MessageReport
        fields = ['id', 'reported_by', 'reported_by_name', 'squad_message', 'direct_message', 'report_type', 'description', 'status', 'created_at']
