from rest_framework import serializers
from .models import Subject, RangeTime


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


    def to_representation(self, instance):
        children = Subject.objects.filter(parent_subject=instance.id)
        subject = {
            "key": instance.id,
            "label": instance.name,
            "data": instance.name,
        }
        children and subject.update({
            "children": [
               self.to_representation(sub) for sub in children
            ]
        })
        return subject


class RangeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangeTime
        fields = '__all__'
