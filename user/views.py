from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SignupSerializer
from .constant import status


@api_view(['POST'])
def sign_up(request):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error"
    errors = None
    data = None
    try:
        # log here, log input, function, t_action
        json_input = request.data
        json_input["customer_id"] = request.user.id
        serializer = SignupSerializer(json_input)
        if serializer.is_valid():
            serializer.save()
            message = "Successfully"
            status_code = status.STATUS_CODE['success']
        else:
            status_code = status.STATUS_CODE["invalid_data"]
            message = status.MESSAGE["invalid_data"]
    except Exception as ex:
        print("log error here ", ex)
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)
