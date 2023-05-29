from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import status


@api_view(['POST'])
def create_post(request):
    post_serializer = PostSerializer(data=request.data)
    if post_serializer.is_valid(raise_exception=True):
        post_serializer.save()
        return Response()