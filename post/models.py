from constant.choice import DAY_CHOICE, STATE, TIME, COMMON
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from user.models import CustomUser
from django.db.models import Q, indexes
from django.contrib.postgres.indexes import BTreeIndex, HashIndex
import datetime


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True)
    parent_subject = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)  # call itself
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    teachers = models.ManyToManyField(
        CustomUser, blank=True, related_name="teachers")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    title = models.CharField(max_length=200)
    content = models.TextField()
    address = models.CharField(max_length=150)
    fee = models.PositiveIntegerField()  # get >= 0 -> 2147483647
    duration = models.PositiveIntegerField(default=0)  # field time : minute
    date_posted = models.DateTimeField(default=timezone.now)
    note = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=100, choices=STATE)

    active = models.BooleanField(default=True)
    approve_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_user")

    class Meta:
        ordering = ('-date_posted',)
        indexes = [
            BTreeIndex(fields=['title', ]),
            BTreeIndex(fields=['fee', ]),
        ]

    @staticmethod
    def get_subject_filter(subjects, all_posts):
        '''
            subjects is list subjects = ['hóa', 'Địa']
        '''
        if subjects == []:
            return all_posts
        else:
            subject_filter = Q(subjects__name__in=subjects)
            return all_posts.filter(subject_filter).distinct()

    @staticmethod
    def get_post_range_time_id(rangetimes):
        ids = []
        for rangetime in rangetimes:
            day, begin_time, end_time = rangetime.split("and")
            rangetime_list = RangeTime.objects.filter(
                Q(day=day) & Q(time_begin=begin_time) & Q(time_end=end_time))
            for rangetime in rangetime_list:
                ids.append(rangetime.post.id)
        return ids

    @staticmethod
    def get_range_time_filter(all_posts, rangetimes):
        if rangetimes == []:
            return all_posts
        else:
            ids = Post.get_post_range_time_id(rangetimes)
            all_posts = all_posts.filter(id__in=ids).distinct()
            return all_posts

    @staticmethod
    def get_fee_filter(all_posts, fromfee, tofee):
        try:
            fromfee = int(fromfee)
            tofee = int(tofee)
            all_posts = all_posts.filter(
                Q(fee__gte=fromfee) & Q(fee__lte=tofee)).distinct()
            return all_posts
        except:
            return all_posts

    @staticmethod
    def get_post_common_range_time_id(commonrangetimes):
        ids = []
        for commonrangetime in commonrangetimes:
            if commonrangetime in COMMON:
                session, day = commonrangetime.split(" ", 1)
                if session == 'Sáng':
                    begin = datetime.datetime.strptime('6:50', '%H:%M').time()
                    end = datetime.datetime.strptime('11:59', '%H:%M').time()
                    rangetime_list = RangeTime.objects.filter(
                        Q(day=day) & Q(time_begin__gte=begin) & Q(time_end__lte=end))
                elif session == "Chiều":
                    begin = datetime.datetime.strptime('12:01', '%H:%M').time()
                    end = datetime.datetime.strptime('23:59', '%H:%M').time()
                    rangetime_list = RangeTime.objects.filter(
                        Q(day=day) & Q(time_begin__gte=begin) & Q(time_end__lte=end))
                for rangetime in rangetime_list:
                    ids.append(rangetime.post.id)
        return ids

    @staticmethod
    def get_common_range_time_filter(all_posts, commonrangetimes):
        if commonrangetimes == []:
            return all_posts
        else:
            ids = Post.get_post_common_range_time_id(commonrangetimes)
            all_posts = all_posts.filter(id__in=ids).distinct()
            return all_posts

    @staticmethod
    def get_address_filter(all_posts, address):
        if address == '':
            return all_posts
        else:
            print(address)
            all_posts = all_posts.filter(address__contains=address)
            return all_posts

    @staticmethod
    def get_registered_posts(user_id):
        try:
            all_posts = Post.objects.filter(teachers=user_id)
            return all_posts
        except:
            return []

    def __str__(self):
        return f"{self.title} -id author {self.author.id} - post id {self.id}"


class RangeTime(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='range_time')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='range_time_user')

    day = models.CharField(max_length=10, choices=DAY_CHOICE)
    time_begin = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return f"day: {self.day}, begin_time:{self.time_begin}, end_time: {self.time_end}"


class PostReview(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post_review')  # có thể null
    comment = models.TextField()
    score = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)  # such as: 90.2, 100.0
    time = models.DateTimeField()
    is_edited = models.BooleanField(default=False)
