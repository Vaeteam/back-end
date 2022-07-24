from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework import status


# TODO login
@api_view(['POST'])
def login(request):
    func_name = "login user"
    # init response
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error"
    errors = None
    data = None
    # get client data
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    try:
        user = authenticate(username=email, password=password)
        if user:
            serializer = LoginSerializer(user)
            data = serializer.data
            status_code = status.HTTP_201_CREATED
            message = "Sucessfully"
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            errors = "Invalid data"
            message = "invalid user or password"
    except Exception as ex:
        # Log here
        print(f"error in {func_name}: ", ex)

    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)
