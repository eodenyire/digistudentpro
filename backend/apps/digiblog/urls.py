from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CommentViewSet, BlogLikeViewSet, BlogFollowViewSet

router = DefaultRouter()
router.register('posts', BlogPostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')
router.register('likes', BlogLikeViewSet, basename='like')
router.register('follows', BlogFollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
