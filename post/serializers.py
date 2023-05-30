from rest_framework import serializers
from .models import Post, PostDetail
from common.models import Subject, RangeTime
from user.models import CustomUser


class PostDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)
    teaching_address = serializers.CharField(max_length=100, required=True)
    fee = serializers.IntegerField(required=True)
    note = serializers.CharField(required=False)
    duration = serializers.CharField(max_length=100, required=True)


class PostSerializer(serializers.Serializer):
    post_detail = PostDetailSerializer()
    user_id = serializers.IntegerField(required=True)
    subject_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    range_time_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    
    def create(self, validated_data):
        validated_post_detail = validated_data.get("post_detail", {})
        post_detail_data = {
            "title": validated_post_detail.get("title"),
            "content": validated_post_detail.get("content"),
            "teaching_address": validated_post_detail.get("teaching_address"),
            "fee": validated_post_detail.get("fee"),
            "note": validated_post_detail.get("note"),
            "duration": validated_post_detail.get("duration")
        }
        post_detail = PostDetail.objects.create(**post_detail_data)
        author = CustomUser.objects.get(id=validated_data.get("user_id"))
        subjects = (Subject.objects.get(id=subject_id) for subject_id in validated_data.get("subject_ids"))
        range_times = (RangeTime.objects.get(id=range_time_id) for range_time_id in validated_data.get("range_time_ids"))

        post = Post.objects.create(post_detail=post_detail, author=author)
        post.subjects.set(subjects)
        post.range_times.set(range_times)

        return post

