from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AdministrativeUnits, Subject, RangeTime
from .serialiers import AdministrativeUnitsSerializer, SubjectSerializer, RangeTimeSerializer


@api_view(['GET'])
def get_subjects(request):
    """Get all subjects."""
    subjects = Subject.objects.filter(parent_subject__isnull=True)
    subject_serializer = SubjectSerializer(subjects, many=True)
    return Response(status=status.HTTP_200_OK, data=subject_serializer.data)

@api_view(['GET'])
def get_range_time(request):
    """Get all range times."""
    range_times = RangeTime.objects.all()
    range_time_serializer = RangeTimeSerializer(range_times, many=True)
    return Response(status=status.HTTP_200_OK, data=range_time_serializer.data) 


@api_view(['GET'])
def get_administrative_unit(request, pk):
    """Get Administrative Units. pk = 0 to get provices"""
    administrative_units = AdministrativeUnits.objects.filter(root=pk) if pk else AdministrativeUnits.objects.filter(root=None)
    administrative_units_serializer = AdministrativeUnitsSerializer(administrative_units, many=True)
    return Response(status=status.HTTP_200_OK, data=administrative_units_serializer.data)
