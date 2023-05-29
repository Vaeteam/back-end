from rest_framework import serializers
from .models import Post, PostDetail
from common.models import Subject, RangeTime
from user.models import CustomUser

class PostDetailSerializer(serializers.Serializer):
    class Meta:
        model = PostDetail
        fields = "__all__"

class PostSerializer(serializers.Serializer):
    post_detail = PostDetailSerializer()

    class Meta:
        model = Post
        fields = "__all__"
    
    def create(self, validated_data):
        post_detail_data = {
            "title": validated_data.get("title"),
            "content": validated_data.get("content"),
            "teaching_address": validated_data.get("teaching_address"),
            "fee": validated_data.get("fee"),
            "note": validated_data.get("note"),
            "duration": validated_data.get("duration")
        }
        post_detail = PostDetail.objects.create(**post_detail_data)
        author = CustomUser.objects.get(id=validated_data.get("user_id"))
        subjects = (Subject.objects.get(id=subject_id) for subject_id in validated_data.get("subject_ids"))
        range_times = (RangeTime.objects.get(id=range_time_id) for range_time_id in validated_data.get("range_time_ids"))


        return Post.objects.create(
            post_detail=post_detail,
            author=author,
            subjects=subjects,
            range_times=range_times
            )

