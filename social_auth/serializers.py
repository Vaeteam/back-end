from rest_framework import serializers
from . import google
from .services import register_social_google_user
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                {'error':'The token is invalid or expired. Please login again.'}
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:   # note HERE
            raise AuthenticationFailed('google client id not right')

        email = user_data.get('email', "")
        first_name = user_data.get('given_name', "")
        last_name = user_data.get("family_name", "")
        return register_social_google_user(email=email, first_name=first_name, last_name=last_name)
