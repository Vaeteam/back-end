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
       
    except CustomUser.DoesNotExist:
        # Todo create new user with default password
        new_user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=settings.DEFAULT_PASSWORD)
        new_user.auth_google = True
        new_user.save()
        return {
            'access_token': new_user.access_token,
            'refresh_token': new_user.refresh_token
        }
    except Exception as e:
        print(f"register_social_google_user {str(e)}")


def register_social_facebook_user(email="", first_name="", last_name="", facebook_id=""):
    user = ""
    try:
        # Todo check user has facebook id exist or not
        user = CustomUser.objects.get(facebook_id=facebook_id)

        return {
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }

    except:
        # check user has email is not exist
        if email == None:
            # create fake email and put it into account, then when login successfully -> check this email is fake or real if fake -> force user update email
            email = CustomUser.gen_random_email()
        else:
            user = CustomUser.objects.filter(email=email).first()

        if bool(user):
            # Facebook account has email already exist in db
            user.auth_facebook = True
            user.facebook_id = facebook_id
            user.save()
            return {
                'access_token': user.access_token,
                'refresh_token': user.refresh_token
            }
        else:
            new_user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=settings.DEFAULT_PASSWORD)
            new_user.auth_facebook = True
            new_user.facebook_id = facebook_id
            new_user.save()
            return  {
                'access_token': new_user.access_token,
                'refresh_token': new_user.refresh_token
            }
