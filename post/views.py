from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import status
from django.forms.models import model_to_dict


@api_view(['POST'])
def create(request):
    """Create new Post."""
    post_serializer = PostSerializer(data=request.data)
    if post_serializer.is_valid(raise_exception=True):
        post_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)