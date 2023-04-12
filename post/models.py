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


class PostDetail(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    address = models.CharField(max_length=150)
    fee = models.PositiveIntegerField()  # get >= 0 -> 2147483647
    note = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)  # field time : minute
    state = models.CharField(max_length=100, choices=STATE)

class Post(models.Model):
    post_detail = models.OneToOneField(PostDetail, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(
        CustomUser, blank=True, related_name="teachers")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    t_create = models.DateTimeField(null=True)
    date_posted = models.DateTimeField(null=True) # default = timezone.now

    active = models.BooleanField(default=True)
    approve_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_user")

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"author {self.author.id} - post id {self.id}"


class RangeTime(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='range_time')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='range_time_user')
    t_create = models.DateTimeField(default=timezone.now)
    day = models.IntegerField(choices=DAY_CHOICE)
    t_begin = models.TimeField()
    t_end = models.TimeField()

    def __str__(self):
        return f"day: {self.day}, begin_time:{self.time_begin}, end_time: {self.time_end}"


class PostReview(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post_review')  # có thể null
    comment = models.TextField()
    score = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)  # such as: 90.2, 100.0
    t_create = models.DateTimeField(default=timezone.now)
    is_edited = models.BooleanField(default=False)


class RequestTeaching(models.Model):
    learner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_learner")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_teacher")
    post = models.ForeignKey(Post, on_delete=Post)
    t_create = models.DateTimeField(default=timezone.now)


class AppliedTeacher(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=Post)
    stage = models.CharField(max_length=100)
    t_create = models.DateTimeField(default=timezone.now)

