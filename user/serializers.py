from rest_framework import serializers
from user.models import CustomUser
from .decentralization import UserGroupPermission
from .services import send_email_account_confirm
from django.contrib.auth.hashers import check_password
from constant import choice
from constant import status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'sex', 'birthday', 'address', 'phone',
                  'email', 'education', 'account_type', 'profile_picture']
        read_only_fields = ['account_type', 'phone', 'email']


class BriefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'sex', 'education', 'account_type', 'profile_picture']


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    account_type = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'password', 'confirm_password', 'sex',
                  'birthday', 'address', 'phone', 'email', 'education', 'account_type']
        read_only_fields = ['account_type']

    def validate(self, data):
        func_name = "validate in signup"
        password = data['password']
        confirm_password = data.pop('confirm_password', None)
        account_type = data.get('account_type', None)

        if len(password) < 8:
            # log e
            raise serializers.ValidationError(
                {'password': "password at least 8 characters / mật khẩu tối thiểu 8 kí tự"},
                status.STATUS_CODE['invalid_data'])

        if password != confirm_password:
            # log e
            raise serializers.ValidationError(
                {'password': "password must match / mật khẩu không khớp nhau"}, status.STATUS_CODE['invalid_data'])

        if account_type not in choice.ACCOUNT_TYPE:
            # log e
            raise serializers.ValidationError(
                {'acount type': "account type invalid / loại tài khoản không hợp lệ"},
                status.STATUS_CODE['invalid_data'])
        return data

    def create(self, validated_data):
        '''
            sign up new user
        '''
        account_type = validated_data.pop("account_type")
        password = validated_data['password']
        new_user = CustomUser(**validated_data)
        new_user.set_password(str(password))
        new_user.is_active = False
        new_user.save()
        if account_type == 'teacher':
            new_user.groups.add(UserGroupPermission.get_teacher_group())
        elif account_type == 'learner':
            new_user.groups.add(UserGroupPermission.get_learner_group())
        send_email_account_confirm(new_user)
        return new_user