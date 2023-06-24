from rest_framework import serializers
from . import google, facebook
from .services import register_social_google_user, register_social_facebook_user
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        func_name = "google_validate_auth_token"
        try:
            user_data = google.Google.validate(auth_token)
            if bool(user_data):
                email = user_data.get('email', "")
                first_name = user_data.get('given_name', "")
                last_name = user_data.get("family_name", "")
                return register_social_google_user(email=email, first_name=first_name, last_name=last_name)
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))

        raise serializers.ValidationError(
            {'error': 'The token is invalid or expired. Please login again.'}
        )


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        func_name = "facebook_validate_auth_token"
        try:
            print("111111111111111")
            user_data = facebook.Facebook.validate(auth_token)
            print("111111111111111 ", user_data)
            if bool(user_data):
                print("111111111111111")
                email = user_data.get('email')
                name = user_data.get('name')
                facebook_id = user_data.get('id')
                print("1111111111111113 ",)
                return register_social_facebook_user(email=email, first_name=name, facebook_id=facebook_id)

            print("1111111111111112")
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))

        raise serializers.ValidationError(
            {'error':'The token is invalid or expired. Please login again.'}
        )
