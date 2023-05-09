from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import SignupSerializer, ResetPassSerializer, LoginSerializer
from .models import CustomUser
from .services import check_email_account_confirmation_token, send_email_password_reset, check_email_reset_password_token
from constant import status


@api_view(('GET',))
def activate(request, uidb64, token):
    func_name = "activate"

    status_code = status.STATUS_CODE["invalid_data"]
    message = status.MESSAGE["invalid_data"]
    errors = True
    data = None

    try:
        check_email_account_confirmation_token(uidb64, token)
        message = "Kích hoạt tài khoản thành công"
        errors = False
        status_code = status.STATUS_CODE['success']
    except Exception as ex:
        print("Error {}: {} ".format(func_name, ex))
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)

@api_view(['POST'])
def check_password_reset(request, uidb64, token):
    func_name = "check_password_reset"

    status_code = status.STATUS_CODE["invalid_data"]
    message = status.MESSAGE["invalid_data"]
    errors = True
    data = None
    password = request.data.get('password', None)
    try:
        if len(password) < 8:
            data = {
                "password": "mật khẩu tối thiểu 8 kí tự"
            }
        else:
            check_email_reset_password_token(uidb64, token, password)
            message = "Đặt lại mật khẩu thành công"
            errors = False

    except Exception as ex:
        print("Error {}: {} ".format(func_name, ex))
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)

@api_view(['POST'])
def sign_up(request):
    func_name = "sign_up"

    status_code = status.STATUS_CODE["invalid_data"]
    message = status.MESSAGE["invalid_data"]
    errors = True
    data = None
    try:
        json_input = request.data
        json_input["customer_id"] = request.user.id
        serializer = SignupSerializer(data=json_input)
        if serializer.is_valid():
            serializer.save()
            message = "Thành công"
            errors = False
            status_code = status.STATUS_CODE['success']
        else:
            data = serializer.errors
    except Exception as ex:
        print("Error {}: {} ".format(func_name, ex))
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)

@api_view(['POST'])
def reset_password(request):
    func_name = "reset_password"

    status_code = status.STATUS_CODE["invalid_data"]
    message = status.MESSAGE["invalid_data"]
    errors = True
    data = None
    try:
        json_input = request.data
        email = request.data.get('email', None)
        user = CustomUser.objects.filter(email=email)
        if not bool(user):
            status_code = status.STATUS_CODE["invalid_data"]
            message = status.MESSAGE["invalid_data"]
            data = {
                "email": "email chưa được đăng ký"
            }
        else:
            user = user[0]
            serializer = ResetPassSerializer(data=json_input, context={"user": user})
            if serializer.is_valid():
                serializer.reset_password(json_input)
                message = "Thành công"
                errors = False
                status_code = status.STATUS_CODE['success']
            else:
                data = serializer.errors
    except Exception as ex:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
        print("Error {}: {} ".format(func_name, ex))

    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }

    return Response(res_dict, status=status_code)

@api_view(['POST'])
def login(request):
    func_name = "login"

    status_code = status.STATUS_CODE["invalid_data"]
    message = status.MESSAGE["invalid_data"]
    errors = True
    data = None
    
    try:
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
        if user:
            serializer = LoginSerializer(user)
            message = "Thành công"
            errors = False
            status_code = status.STATUS_CODE['success']
            data = serializer.data
        else:
            status_code = status.STATUS_CODE["invalid_data"]
            message = status.MESSAGE["invalid_data"]
            data = {
                "email": "tên đăng nhập hoặc mật khẩu không đúng"
            }
    except Exception as ex:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Internal server error"
        print("Error {}: {} ".format(func_name, ex))

    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }

    return Response(res_dict, status=status_code)
