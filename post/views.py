import logging
from any_case import converts_keys
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer, PostDetailSerializer
from rest_framework import status


logger = logging.getLogger(__name__)

@api_view(['POST'])
def create(request):
    """ Create new Post """
    try:
        logger.info(f"Create Post with data {str(request.data)}")
        snake_case_request_data = converts_keys(request.data, case='snake')
        post_serializer = PostDetailSerializer(data=snake_case_request_data)

        if post_serializer.is_valid(raise_exception=True):
            post_instance = post_serializer.save()
            response_data = PostSerializer(post_instance).data
            logger.info(f"Created Post with data {str(response_data)}")
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.info(f"Create Post failed with error {str(e)}")
        return Response(data=str(e), status=status.HTTP_501_NOT_IMPLEMENTED)