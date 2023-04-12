from rest_framework import serializers
from user.models import CustomUser


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('access_token', 'refresh_token')
        read_only_fields = ['access_token', 'refresh_token']
