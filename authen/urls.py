from django.urls import path, include
from .views import login

urlpatterns = [
    path('users/login/', login)
]
