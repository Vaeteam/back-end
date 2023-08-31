from django.urls import path
from .views import get_administrative_unit, get_subjects, get_range_time

urlpatterns = [
    path('subjects/', get_subjects, name="get_subjects"),
    path('range_times/', get_range_time, name="get_range_time"),
    path('administrative_unit/<int:pk>/', get_administrative_unit, name="get_administrative_unit"),
]
