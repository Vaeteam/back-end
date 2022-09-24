from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializers
from rest_framework import status


@api_view(['GET'])
def get_posts(request):

    postSerializers = PostSerializers(instance=None, data=request.data)
    # validate data input
    # if postSerializers.is_valid(raise_exception=True):
    #     return Response("not ok")

    data = postSerializers.get_posts_filter(request.data)

    print("obj: ", data)
    return Response("ok")
    # posts = service_get_posts(
    #     subjects, rangetimes, fromfee, tofee, commonrangetimes, address)

    # paginator = CustomPropertyPagination()
    # posts = paginator.paginate_queryset(posts, request)
    # serializers = PostSerializers(posts, many=True)
    #
    # return Response(format_response(status_code=status.STATUS_CODE["success"], message=status.MESSAGE['success'],
    #                                 data=paginator.get_paginated_response(serializers.data)))
