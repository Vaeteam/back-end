from constant.choice import STATE
from django.db import models
from django.utils import timezone
from user.models import CustomUser
from common.models import Subject, RangeTime


class PostDetail(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    teaching_address = models.CharField(max_length=150)
    fee = models.PositiveIntegerField()
    note = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=50)


class Post(models.Model):
    post_detail = models.OneToOneField(PostDetail, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(CustomUser, blank=True, related_name="teachers")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    range_times = models.ManyToManyField(RangeTime)
    approve_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_user")

    updated_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(default=timezone.now) # default = timezone.now
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=100, choices=STATE, default=STATE[0][0])

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"author {self.author.id} - post id {self.id}"


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

