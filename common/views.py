from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Subject, RangeTime
from .serialiers import SubjectSerializer, RangeTimeSerializer


@api_view(['GET'])
def get_subjects(request):
    """Get all subjects."""
    subjects = Subject.objects.all()
    subject_serializer = SubjectSerializer(subjects, many=True)
    return Response(status=status.HTTP_200_OK, data=subject_serializer.data)

@api_view(['GET'])
def get_range_time(request):
    """Get all range times."""
    range_times = RangeTime.objects.all()
    range_time_serializer = RangeTimeSerializer(range_times, many=True)
    return Response(status=status.HTTP_200_OK, data=range_time_serializer.data) 
