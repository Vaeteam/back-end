from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import SignupSerializer, ResetPassSerializer
from .models import CustomUser
from .services import check_email_account_confirmation_token, send_email_password_reset, check_email_reset_password_token
from constant import status


@api_view(('GET',))
def activate(request, uidb64, token):
    check_email_account_confirmation_token(uidb64, token)
    return Response("Confirm email account successfully")

@api_view(['POST'])
def check_password_reset(request, uidb64, token):
    password = request.data.get('password', None)
    if len(password) < 8:
        return Response({'error': "password at least 8 characters / mật khẩu tối thiểu 8 kí tự"})

    check_email_reset_password_token(uidb64, token, password)
    return Response("Reset account password successfully")

@api_view(['POST'])
def sign_up(request):
    func_name = "sign_up"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error"
    errors = None
    data = None
    try:
        json_input = request.data
        json_input["customer_id"] = request.user.id
        serializer = SignupSerializer(data=json_input)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = "Successfully"
            status_code = status.STATUS_CODE['success']
        else:
            status_code = status.STATUS_CODE["invalid_data"]
            message = status.MESSAGE["invalid_data"]
    except Exception as ex:
        print("Error {}: {} ".format(func_name, ex))
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)

@api_view(['POST'])
def reset_password(request):
    try:
        json_input = request.data
        email = request.data.get('email', None)
        user = CustomUser.objects.get(email=email)
        serializer = ResetPassSerializer(data=json_input, context={"user": user})
        if serializer.is_valid(raise_exception=True):
            serializer.reset_password(json_input)
    except:
        return Response({'error': 'email is not sign up'})

    return Response({'success': 'email have been sent'})

@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
        if user:
            serializer = LoginSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'Wrong password or username'})
    except:
        return Response({'error': 'Có lỗi trong quá trình xử lý'})

