import logging
from any_case import converts_keys
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer, PostDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from common.utils import form_response

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    """ Create new Post """
    try:
        user_info = request.user
        logger.info(f"Creating Post with data {str(request.data)}")
        snake_case_request_data = converts_keys(request.data, case='snake')
        post_serializer = PostDetailSerializer(data=snake_case_request_data)

        if post_serializer.is_valid(raise_exception=True):
            post_instance = post_serializer.save()
            response_data = PostSerializer(post_instance).data
            logger.info(f"Created Post with data {str(response_data)}")
            return Response(data=form_response(
                                data=response_data, 
                                message="Bài Tuyển Gia Sư", 
                                detail="bài tuyển gia sư của bạn đã được tạo thành công, hãy đợi gia sư đến ứng tuyển"
                                ), 
                            status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Create Post failed with error {str(e)}")
        return Response(data=form_response(
            message=e.__class__.__name__, 
            detail=str(e)
            ), 
            status=status.HTTP_501_NOT_IMPLEMENTED)
