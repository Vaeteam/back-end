from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('signup/', views.sign_up),
    path('reset_pass/', views.reset_password)
]