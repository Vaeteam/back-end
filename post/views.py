from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializers
from rest_framework import status


@api_view(['GET'])
def get_posts(request):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error"
    errors = None
    data = None
    try:
        json_input = request.data
        json_input["customer_id"] = request.user.id
        postSerializers = PostSerializers(instance=None, data=json_input)
        querySet = postSerializers.get_posts_filter(request.data)
        serializers = PostSerializers(querySet, many=True)
        message = "Successfully"
        status_code = status.HTTP_200_OK
        data = serializers.data
        # log here, log use_id - t_call_api, func_name
    except Exception as ex:
        print("log error here ", ex)
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)

