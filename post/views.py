from any_case import converts_keys
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer, PostDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    """Create new Post."""
    user_info = request.user # get user object
    snake_case_request_data = converts_keys(request.data, case='snake')
    post_serializer = PostDetailSerializer(data=snake_case_request_data)

    if post_serializer.is_valid(raise_exception=True):
        post_instance = post_serializer.save()
        response_data = PostSerializer(post_instance).data
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    