"""
URL configuration for comments app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]

