from django.urls import path
from .views import create_post, list_post

urlpatterns = [
    path('create/', create_post),
    path('list/', list_post),
]
