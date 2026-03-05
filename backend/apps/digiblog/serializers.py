from rest_framework import serializers
from .models import BlogPost, Comment, BlogLike, BlogFollow


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'author_name', 'category', 'content', 'excerpt',
            'featured_image', 'status', 'is_featured', 'views_count', 'likes_count',
            'comments_count', 'meta_description', 'tags', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'views_count', 'likes_count', 'comments_count']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'content', 'parent', 'is_approved', 'is_flagged', 'created_at', 'updated_at', 'replies']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class BlogLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = BlogLike
        fields = ['id', 'post', 'user', 'user_name', 'created_at']


class BlogFollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.CharField(source='follower.get_full_name', read_only=True)
    following_name = serializers.CharField(source='following.get_full_name', read_only=True)
    
    class Meta:
        model = BlogFollow
        fields = ['id', 'follower', 'follower_name', 'following', 'following_name', 'created_at']
