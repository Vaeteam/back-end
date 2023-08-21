from rest_framework import serializers
from user.models import Certificate, CustomUser
from .services import send_email_account_confirm
from django.contrib.auth.hashers import check_password
from constant import choice
from constant import status
from .services import send_email_password_reset
from post.serializers import PostSerializer
from common.serialiers import SubjectSerializer, RangeTimeSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'sex', 'birthday', 'address', 'phone',
                  'email', 'education', 'account_type', 'profile_picture']
        read_only_fields = ['account_type', 'phone', 'email']


class BriefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'sex', 'education', 'account_type', 'profile_picture']


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def to_representation(self, instance):
        try:
            return super().to_representation(instance)
        except Exception as e:
            return {'error': str(e)}

    def validate(self, data):
        password = data['password']
        confirm_password = data.pop('confirm_password', None)

        if len(password) < 8:
            raise serializers.ValidationError(
                {'password': "password at least 8 characters / mật khẩu tối thiểu 8 kí tự"},
                status.STATUS_CODE['invalid_data'])

        if password != confirm_password:
            raise serializers.ValidationError(
                {'password': "password must match / mật khẩu không khớp nhau"}, status.STATUS_CODE['invalid_data'])

        return data

    def create(self, validated_data):
        '''
            sign up new user
        '''
        password = validated_data['password']
        email = validated_data['email']
        # new_user = CustomUser(**validated_data)
        new_user = CustomUser()
        new_user.first_name = validated_data['first_name']
        new_user.last_name = validated_data['last_name']
        new_user.email = new_user.gen_random_email()
        new_user.set_password(str(password))
        new_user.is_active = False
        new_user.save()

        # Cần tách thread ra để gọi 1 thread riêng
        send_email_account_confirm(new_user, email)
        return new_user


class ResetPassSerializer(serializers.Serializer):
    email = serializers.CharField(
        style={'input_type': 'email'}, write_only=True)


    def reset_password(self, validated_data):
        email = validated_data['email']
        user = self.context.get("user")

        # Cần tách thread ra để gọi 1 thread riêng
        send_email_password_reset(user)

        return user

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields= ('access_token', 'refresh_token', 'id', 'first_name', "last_name", "email", "is_teacher")

        read_only_fields = ['access_token', 'refresh_token']


class CertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        exclude = ('user',)

    
    def to_representation(self, instance):
        return super().to_representation(instance)


class GetProfileSerializer(serializers.ModelSerializer):

    # many params to get list in 1-n or n-n relation, required params is if pass None then ok
    certificate = CertSerializer(many=True, required=False) 
    post_management = PostSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    range_times = RangeTimeSerializer(many=True)

    class Meta:
        model = CustomUser 
        exclude = ('is_validate_phone', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'auth_google', 'auth_facebook', 'facebook_id', 'is_staff', 'is_active', 'date_joined')


    def to_representation(self, instance):
        try:
            # Todo get context parameter
            context = self.context
            user_info = context["user_info"]
            print("2. ", user_info)

            data = super().to_representation(instance)

            
            if isinstance(instance, CustomUser) and instance.id == user_info.id: 
                # Todo get detail data
                pass
            else:
                # note 
                # 1. hide a part of email
                # 2. hide a part of phone
                # 3. hide address 
                # 4. in middleware, catch the inactive user case

                # Todo get general data

                # get guest personal info

                # get guest certs info

                pass
            return data
            return {
                'personal_info': "test"
            }
        except Exception as ex:
            print(ex)
            return {}

