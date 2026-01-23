from django.db import models
from django.utils.text import slugify


class Squad(models.Model):
    """Group chats (Squads) for topic-based communities"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    topic = models.CharField(max_length=100)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_squads')
    members = models.ManyToManyField('accounts.User', related_name='squads', through='SquadMembership')
    is_public = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(default=100)
    avatar = models.ImageField(upload_to='squad_avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SquadMembership(models.Model):
    ROLE_CHOICES = [('admin', 'Admin'), ('moderator', 'Moderator'), ('member', 'Member')]
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['squad', 'user']
    
    def __str__(self):
        return f"{self.user.get_full_name()} in {self.squad.name}"


class Message(models.Model):
    """Messages in Squad group chats"""
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='squad_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    is_flagged = models.BooleanField(default=False)
    flagged_reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['squad', 'created_at'])]
    
    def __str__(self):
        return f"{self.sender.get_full_name()} in {self.squad.name}"


class DirectMessage(models.Model):
    """1-on-1 direct messages"""
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to='dm_attachments/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_flagged = models.BooleanField(default=False)
    flagged_reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['sender', 'recipient', 'created_at'])]
    
    def __str__(self):
        return f"{self.sender.get_full_name()} → {self.recipient.get_full_name()}"


class MessageReport(models.Model):
    REPORT_TYPE_CHOICES = [('spam', 'Spam'), ('harassment', 'Harassment'), ('inappropriate', 'Inappropriate'), ('other', 'Other')]
    STATUS_CHOICES = [('pending', 'Pending'), ('reviewed', 'Reviewed'), ('resolved', 'Resolved'), ('dismissed', 'Dismissed')]
    
    reported_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='message_reports')
    squad_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    direct_message = models.ForeignKey(DirectMessage, on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        reporter = self.reported_by.get_full_name() if self.reported_by else 'Unknown'
        return f"Report by {reporter}"
