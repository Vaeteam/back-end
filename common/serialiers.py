from rest_framework import serializers
from .models import Subject, RangeTime


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class RangeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangeTime
        fields = '__all__'
