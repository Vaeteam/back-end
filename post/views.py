from any_case import converts_keys
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostDetailSerializer
from rest_framework import status


@api_view(['POST'])
def create(request):
    """Create new Post."""
    snake_case_request_data = converts_keys(request.data, case='snake')
    post_serializer = PostDetailSerializer(data=snake_case_request_data)
    if post_serializer.is_valid(raise_exception=True):
        post_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)