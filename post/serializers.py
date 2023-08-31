from rest_framework import serializers
from .models import Post, PostDetail
from common.models import Subject, RangeTime
from user.models import CustomUser
from common.serialiers import AdministrativeUnitsSerializer, RangeTimeSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    range_times = RangeTimeSerializer(many=True)
    subjects = serializers.ListField()
    teaching_province = AdministrativeUnitsSerializer(required=False)
    teaching_district = AdministrativeUnitsSerializer(required=False)
    teaching_ward = AdministrativeUnitsSerializer(required=False)

    class Meta:
        model = PostDetail
        fields = '__all__'
    
    def to_internal_value(self, data):
        modified_data = data.copy()
        modified_data['range_times'] = data['shifts']
        modified_data['subjects'] = [key for key, checking_status in data['selected_subjects'].items()
                                     if checking_status['checked']]
        validated_data = super().to_internal_value(modified_data)
        validated_data.get("teaching_province") and validated_data.update({"teaching_province": validated_data.get("teaching_province")["id"]})
        validated_data.get("teaching_district") and validated_data.update({"teaching_district": validated_data.get("teaching_district")["id"]})
        validated_data.get("teaching_ward") and validated_data.update({"teaching_ward": validated_data.get("teaching_ward")["id"]})
        return validated_data

    def create(self, validated_data):
        if not validated_data:
            raise serializers.ValidationError("Data is not valid.")
        subjects_ids = validated_data.pop('subjects', [])
        range_times_data = validated_data.pop('range_times', [])

        teaching_province = validated_data.pop('teaching_province')
        teaching_district = validated_data.pop('teaching_district')
        teaching_ward = validated_data.pop('teaching_ward')

        post_detail = PostDetail.objects.create(**validated_data)
        learner = CustomUser.objects.get(id=1)
        post = Post.objects.create(post_detail=post_detail, 
                                   author=learner, 
                                   teaching_province_id=teaching_province,
                                   teaching_district_id=teaching_district,
                                   teaching_ward_id=teaching_ward,)
        subjects_to_add = Subject.objects.filter(pk__in=subjects_ids)
        post.subjects.add(*subjects_to_add)

        for range_time_data in range_times_data:
            range_time = RangeTime.objects.create(**range_time_data)
            post.range_times.add(range_time)

        return post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
