from constant.choice import SEX
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager
from django.utils import timezone
from common.models import RangeTime
import jwt
import random
import string


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=6, choices=SEX, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150, null=True, blank=True)

    auth_google = models.BooleanField(default=False)
    auth_facebook = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    range_times = models.ManyToManyField(RangeTime)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def fullname(self):
        return self.last_name + self.first_name

    @staticmethod
    def gen_random_email():
        return  "RANDOM_"  + "".join(random.choices(string.ascii_uppercase + string.digits, k=20)) + "@gmail.com"

    @property
    def access_token(self):
        token = jwt.encode({'id': self.id, 'type': 'access_token', 'first_name': self.first_name, 'email': self.email,
                            'exp': datetime.utcnow() + timedelta(days=7)}, settings.SECRET_KEY, algorithm='HS256')
        return token

    @property
    def refresh_token(self):
        token = jwt.encode({'id': self.id, 'type': 'refresh_token', 'first_name': self.first_name, 'email': self.email,
                            'exp': datetime.utcnow() + timedelta(days=27)}, settings.SECRET_KEY, algorithm='HS256')
        return token


class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="certificate")
    cert_name = models.CharField(max_length=100)
    cert_url = models.CharField(max_length=100)
