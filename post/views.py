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
        postSerializers = PostSerializers(instance=None, data=request.data)
        querySet = postSerializers.get_posts_filter(request.data)
        serializers = PostSerializers(querySet, many=True)
        message = "Successfully"
        status_code = status.HTTP_200_OK
        data = serializers.data
    except Exception as ex:
        print("log here ", ex)
    res_dict = {
        "message": message,
        "errors": errors,
        "data": data
    }
    return Response(res_dict, status=status_code)

