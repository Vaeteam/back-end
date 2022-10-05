from curses import keyname
from post.models import Post, RangeTime, Subject
from rest_framework import serializers
from constant.choice import DAY
from constant import status
from .services import is_null_or_empty, is_null_or_empty_params
from django.db.models import Q

import datetime


class RangeTimeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RangeTime
        fields = ['day', 'time_begin', 'time_end']


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class PostSerializers(serializers.ModelSerializer):
    subjects = SubjectSerializers(many=True)
    range_time = RangeTimeSerializers(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'address', 'content', 'fee', 'duration',
                  'note', 'range_time', 'subjects', 'teachers', 'date_posted']
        read_only_fields = ['date_posted', 'teachers']

    def to_representation(self, instance):
        representation = super(PostSerializers, self).to_representation(instance)
        representation['date_posted'] = instance.date_posted.strftime("%Y-%m-%d %H:%M:%S")
        return representation

    def validate_fee(self, fee):
        try:
            from_fee = fee.get("from_fee")
            to_fee = fee.get("to_fee")
            if not isinstance(from_fee, int) and not isinstance(to_fee, int):
                raise serializers.ValidationError(
                    'field fee must be integer / tiền phí phải là số', status.STATUS_CODE['invalid_data'])
        except:
            raise serializers.ValidationError(
                'field fee must be integer / tiền phí phải là số', status.STATUS_CODE['invalid_data'])
        return fee

    def validate_duration(self, duration):
        try:
            duration = int(duration)
        except:
            raise serializers.ValidationError(
                'field duration must be integer / thời gian dạy trong suốt phải là số',
                status.STATUS_CODE['invalid_data'])
        return duration

    def validate_subjects(self, subjects):
        if len(subjects) != 0:
            for subject in subjects:
                if not isinstance(subject, int):
                    raise serializers.ValidationError(
                        'subject invalid / môn học không hợp lệ', status.STATUS_CODE['invalid_data'])
            return subjects
        raise serializers.ValidationError(
            'subject invalid / môn học không hợp lệ', status.STATUS_CODE['invalid_data'])

    def validate_days(self, days):
        if len(days) != 0:
            for day in days:
                if not isinstance(day, int):
                    raise serializers.ValidationError(
                        'day invalid / ngày không hợp lệ', status.STATUS_CODE['invalid_data'])
            return days
        raise serializers.ValidationError(
            'day invalid / ngày không hợp lệ', status.STATUS_CODE['invalid_data'])

    def validate_range_time(self, multi_range_time):
        '''
            Check that start is before finish.
        '''
        if len(multi_range_time) != 0:
            for range_time in multi_range_time:
                try:
                    day = range_time['day']
                    time_begin = range_time['time_begin']
                    time_end = range_time['time_end']

                    time_begin = datetime.datetime.strptime(f"27/10/2000 {time_begin}", "%d/%m/%Y %H:%M:%S").time()
                    time_end = datetime.datetime.strptime(f"27/10/2000 {time_end}", "%d/%m/%Y %H:%M:%S").time()

                    if day not in DAY:
                        raise serializers.ValidationError(
                            'teaching day invalid / ngày dạy không hợp lệ', status.STATUS_CODE['invalid_data'])
                    if not isinstance(time_begin, datetime.time) and not isinstance(time_end, datetime.time):
                        raise serializers.ValidationError(
                            'teaching day invalid / ngày dạy không hợp lệ', status.STATUS_CODE['invalid_data'])
                    if time_begin > time_end:
                        raise serializers.ValidationError(
                            'time invalid / thời gian dạy không hợp lệ', status.STATUS_CODE['invalid_data'])
                except Exception as e:
                    print("exception: ", e)
                    raise serializers.ValidationError(
                        'time invalid / thời gian dạy không hợp lệ', status.STATUS_CODE['invalid_data'])
            return multi_range_time
        raise serializers.ValidationError(
            'time invalid / thời gian dạy không hợp lệ', status.STATUS_CODE['invalid_data'])

    def validate(self, data):
        user = self.context['user']
        account_type = user.account_type
        if 'teacher' not in account_type:
            raise serializers.ValidationError(
                {'error': 'must be as teacher / phải có quyền giáo viên'}, status.STATUS_CODE['unauthorized'])
        return data

    def custom_validate(self, data):
        fee = data.get("fee", {})
        range_times = data.get('range_times', [])
        if len(fee) > 0:
            fee = self.validate_fee(fee)
        if len(range_times) > 0:
            range_times = self.validate_range_time(range_times)

    def get_posts_filter(self, data):
        self.custom_validate(data)

        keyword = data.get("keyword", "")  # title, subjects, address, author_name
        range_times = data.get('range_times', [])
        fee = data.get("fee", {})
        from_fee = fee.get("from_fee")
        to_fee = fee.get("to_fee")
        common_range_times = data.get('common_range_times', [])

        # filter
        query = ""
        is_add = False
        if not is_null_or_empty(keyword):
            keyword = keyword.lower()
            query = Q(title__contains=keyword) | Q(subjects__name__contains=keyword) | Q(address__contains=keyword) | Q(
                author__first_name=keyword) | Q(author__last_name=keyword)
            is_add = True

        if not is_null_or_empty_params(from_fee, to_fee):
            sub_query = Q(fee__gte=from_fee) & Q(fee__lte=to_fee)
            if is_add:
                query = query & sub_query
            else:
                query = sub_query

        if len(range_times) != 0:
            rangetimes_id = Post.get_post_range_time_id(range_times)
            sub_query = Q(id__in=rangetimes_id)
            if is_add:
                query = query & sub_query
            else:
                query = sub_query

        if len(common_range_times) != 0:
            pass

        if query != "":
            data = Post.objects.filter(query)
        else:
            data = Post.objects.all()
        return data
