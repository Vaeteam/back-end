from django.urls import path, include
from .views import get_posts

urlpatterns = [
    path('get_posts/', get_posts)
]
