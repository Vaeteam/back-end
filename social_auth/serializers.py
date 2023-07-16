import logging
from rest_framework import serializers
from . import google, facebook
from .services import register_social_google_user, register_social_facebook_user
from rest_framework.exceptions import AuthenticationFailed


logger = logging.getLogger(__name__)
class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        func_name = "google_validate_auth_token"
        try:
            user_data = google.Google.validate(auth_token)
            logger.info(f'VALIDATE USER LOGGING: validate GG login get value {str(user_data)}')
            email = user_data['email']
            first_name = user_data['given_name']
            last_name = user_data["family_name"]
            return register_social_google_user(email=email, first_name=first_name, last_name=last_name)
        except Exception as e:
            logger.error("Error in {}: {}".format(func_name, e))

            raise serializers.ValidationError(
                {'error': str(e)}
            )


class FacebookSocialAuthSerializer(serializers.Serializer):
    fb_access_token = serializers.CharField()

    def validate_fb_access_token(self, fb_access_token):
        func_name = "facebook_validate_auth_token"
        try:
            user_data = facebook.Facebook.validate(fb_access_token)
            if bool(user_data):
                email = user_data.get('email')
                name = user_data.get('name')
                facebook_id = user_data.get('id')
                return register_social_facebook_user(email=email, first_name=name, facebook_id=facebook_id)
        except Exception as e:
            print("Error in {}: {}".format(func_name, e))

        raise serializers.ValidationError(
            {'error':'The token is invalid or expired. Please login again.'}
        )
