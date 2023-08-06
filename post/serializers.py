from rest_framework import serializers
from .models import Post, PostDetail
from common.models import Subject, RangeTime
from user.models import CustomUser
from common.serialiers import RangeTimeSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    range_times = RangeTimeSerializer(many=True)
    subjects = serializers.ListField()

    class Meta:
        model = PostDetail
        fields = '__all__'
    
    def to_internal_value(self, data):
        modified_data = data.copy()
        modified_data['range_times'] = data['shifts']
        return super().to_internal_value(modified_data)

    def create(self, validated_data):
        if not validated_data:
            print(self.errors)
            raise serializers.ValidationError("Data is not valid.")
        subjects_ids = validated_data.pop('subjects', [])
        range_times_data = validated_data.pop('range_times', [])
        post_detail = PostDetail.objects.create(**validated_data)
        leaner = CustomUser.objects.get(id=1)
        post = Post.objects.create(post_detail=post_detail, author=leaner)

        subjects_to_add = Subject.objects.filter(pk__in=subjects_ids)
        post.subjects.add(*subjects_to_add)

        for range_time_data in range_times_data:
            range_time = RangeTime.objects.create(**range_time_data)
            post.range_times.add(range_time)

        return post
