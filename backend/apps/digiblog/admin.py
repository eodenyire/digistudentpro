from django.contrib import admin
from .models import BlogPost, Comment, BlogLike, BlogFollow


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views_count', 'likes_count', 'published_at']
    list_filter = ['status', 'category', 'is_featured', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'likes_count', 'comments_count', 'created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_approved', 'is_flagged', 'created_at']
    list_filter = ['is_approved', 'is_flagged', 'created_at']
    search_fields = ['content', 'author__email', 'post__title']


@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at']


@admin.register(BlogFollow)
class BlogFollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
