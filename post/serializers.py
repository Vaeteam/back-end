from post.models import Post, RangeTime, Subject
from rest_framework import serializers
from constant.choice import DAY
from .services import is_null_or_empty
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

    def get_posts_filter(self, data):

        subjects = data.get('subject', [])
        rangetimes = data.get('range_time', [])
        fee = data.get("fee")
        common_range_times = data.get('common_range_times', [])
        address = data.get('address')
        print(subjects, rangetimes, fee, common_range_times, address)
        # validate

        # filter
        query = ""
        if not is_null_or_empty(subjects):
            query = Q(subjects in subjects)
        if not is_null_or_empty(rangetimes):
            condition_rangetime = ""
            for rangetime in rangetimes:
                day = rangetime.get("day")
                time_begin = rangetime.get("time_begin")
                time_end = rangetime.get("time_end")
                condition_rangetime = Q(day=day) & Q(time_begin__gte=time_begin) & Q(time_end__lte=time_end)
                if is_null_or_empty(condition_rangetime):
                    pass
                else:
                    condition_rangetime = condition_rangetime + Q()

        query = Q(firstname='Emil') | Q(firstname='Tobias')
        filter(query)
        return data