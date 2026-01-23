from django.contrib import admin
from .models import Squad, SquadMembership, Message, DirectMessage, MessageReport


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'created_by', 'is_public', 'max_members', 'created_at']
    list_filter = ['is_public', 'topic', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SquadMembership)
class SquadMembershipAdmin(admin.ModelAdmin):
    list_display = ['squad', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['squad__name', 'user__email']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['squad', 'sender', 'is_flagged', 'created_at']
    list_filter = ['is_flagged', 'created_at']
    search_fields = ['content', 'sender__email']


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'is_read', 'is_flagged', 'created_at']
    list_filter = ['is_read', 'is_flagged', 'created_at']
    search_fields = ['content', 'sender__email', 'recipient__email']


@admin.register(MessageReport)
class MessageReportAdmin(admin.ModelAdmin):
    list_display = ['reported_by', 'report_type', 'status', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['description', 'reported_by__email']
