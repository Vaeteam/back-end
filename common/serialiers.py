import datetime
from rest_framework import serializers
from .models import AdministrativeUnits, Subject, RangeTime


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


def modify_time(time_string):
    time_object = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return time_object.time()


class RangeTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangeTime
        fields = '__all__'

    def to_internal_value(self, data):
        data['start_time'] = modify_time(data['start_time'])
        data['end_time'] = modify_time(data['end_time'])
        return super().to_internal_value(data)


class AdministrativeUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeUnits
        fields = "__all__"

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        isinstance(data.get("id"), int) and validated_data.update({"id": data.get("id")})
        return validated_data
    