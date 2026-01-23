"""
URL configuration for DigiStudentPro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

# API Router
router = DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include([
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
        path('accounts/', include('apps.accounts.urls')),
        path('digiguide/', include('apps.digiguide.urls')),
        path('digilab/', include('apps.digilab.urls')),
        path('digichat/', include('apps.digichat.urls')),
        path('digiblog/', include('apps.digiblog.urls')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "DigiStudentPro Administration"
admin.site.site_title = "DigiStudentPro Admin Portal"
admin.site.index_title = "Welcome to DigiStudentPro Administration"
