from constant.choice import SEX
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
import jwt


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    sex = models.CharField(max_length=6, choices=SEX, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, null=True, blank=True)

    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def access_token(self):
        token = jwt.encode({'id': self.id, 'type': 'access_token', 'first_name': self.first_name, 'email': self.email,
                            'exp': datetime.utcnow() + timedelta(days=1)}, settings.SECRET_KEY, algorithm='HS256')
        return token

    @property
    def refresh_token(self):
        token = jwt.encode({'id': self.id, 'type': 'refresh_token', 'first_name': self.first_name, 'email': self.email,
                            'exp': datetime.utcnow() + timedelta(days=27)}, settings.SECRET_KEY, algorithm='HS256')
        return token
