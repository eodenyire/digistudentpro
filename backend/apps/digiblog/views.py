from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost, Comment, BlogLike, BlogFollow
from .serializers import BlogPostSerializer, CommentSerializer, BlogLikeSerializer, BlogFollowSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.select_related('author').filter(status='published')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'is_featured']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['published_at', 'views_count', 'likes_count']
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'parent']


class BlogLikeViewSet(viewsets.ModelViewSet):
    queryset = BlogLike.objects.select_related('user', 'post').all()
    serializer_class = BlogLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'user']


class BlogFollowViewSet(viewsets.ModelViewSet):
    queryset = BlogFollow.objects.select_related('follower', 'following').all()
    serializer_class = BlogFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['follower', 'following']
