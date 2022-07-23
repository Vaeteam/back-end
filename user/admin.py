from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'phone', 'email', 'first_name', 'last_name', 'sex', 'date_joined', 'last_login', 'is_active',
        'is_staff', 'is_superuser')
    search_fields = (
        'id', 'phone', 'email', 'username', 'date_joined', 'last_login', 'auth_google', 'auth_facebook', 'is_active',
        'is_staff', 'is_superuser')
