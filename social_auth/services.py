from django.contrib.auth import authenticate
from  user.models import CustomUser
import os
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


def register_social_google_user(email="", first_name="", last_name=""):
    # Todo check user with email input exist or not
    # If exist return access and refresh token, if no create account first then return token
    try:
        # Todo if exist email in db
        user = CustomUser.objects.get(email=email)
        if user.auth_google == False:
            user.is_active  = True
            user.auth_google = True
            user.save()
        
        return {
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }
       
    except:
        # If email not in db
        # Todo create new user with default password
        new_user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password= settings.DEFAULT_PASSWORD)
        new_user.is_active  = True
        new_user.auth_google = True
        new_user.save()
        return {
            'access_token': new_user.access_token,
            'refresh_token': new_user.refresh_token
        }
