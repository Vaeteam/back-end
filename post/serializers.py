from rest_framework import serializers
from .models import Post, PostDetail, PostReview
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
        modified_data['subjects'] = [key for key, checking_status in data['selected_subjects'].items()
                                     if checking_status['checked']]
        return super().to_internal_value(modified_data)

    def create(self, validated_data):
        if not validated_data:
            raise serializers.ValidationError("Data is not valid.")
        subjects_ids = validated_data.pop('subjects', [])
        range_times_data = validated_data.pop('range_times', [])
        post_detail = PostDetail.objects.create(**validated_data)
        learner = CustomUser.objects.get(id=1)
        post = Post.objects.create(post_detail=post_detail, author=learner)

        subjects_to_add = Subject.objects.filter(pk__in=subjects_ids)
        post.subjects.add(*subjects_to_add)

        for range_time_data in range_times_data:
            range_time = RangeTime.objects.create(**range_time_data)
            post.range_times.add(range_time)
 
        return post


class PostReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReview
        fields = '__all__'

            
class PostSerializer(serializers.ModelSerializer):
    post_review = PostReviewSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        context = self.context
        user_info = context['user_info']
        print("the instance: ", instance)
        # return super().to_representation(instance)

        if isinstance(instance, CustomUser) and instance.id == user_info.id:
            # Todo get the posts belonged to post's author
            print("the instance after 1: ", instance)
            return super().to_representation(instance)
        else:
            # Todo get the posts that teacher teached
            # overide instance
            instance = Post.objects.filter(approve_user=user_info.id)
            print("the instance after 2: ", instance)
            return super().to_representation(instance)

