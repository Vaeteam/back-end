from django.urls import path
from .views import get_subjects, get_range_time

urlpatterns = [
    path('subjects/', get_subjects, name="get_subjects"),
    path('range_times/', get_range_time, name="get_range_time"),
]
