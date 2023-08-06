from constant.choice import STATE, SEX, TEACHING_LOCATION, TEACHING_TIME_UNIT, EDUCATION, YEAR_EXP
from django.db import models
from django.utils import timezone
from user.models import CustomUser
from common.models import Subject, RangeTime


class PostDetail(models.Model):
    learner_name = models.CharField(max_length=100)
    learner_sex = models.CharField(max_length=6, choices=SEX)
    learner_birth_year = models.PositiveIntegerField(null=True, blank=True)
    teaching_location = models.CharField(max_length=20, choices=TEACHING_LOCATION)
    total_teaching_time = models.PositiveIntegerField()
    total_teaching_time_unit = models.CharField(max_length=20, choices=TEACHING_TIME_UNIT)
    teaching_address = models.CharField(max_length=150, blank=True, null=True)
    teaching_fee = models.PositiveIntegerField()
    teaching_fee_unit = models.CharField(max_length=20, choices=TEACHING_TIME_UNIT)
    reuqest_teacher_sex = models.CharField(max_length=6, choices=SEX)
    reuqest_teacher_year_old_from = models.PositiveIntegerField(blank=True, null=True)
    reuqest_teacher_year_old_to = models.PositiveIntegerField(blank=True, null=True)
    request_teacher_education = models.CharField(max_length=20, blank=True, null=True, choices=EDUCATION)
    request_teacher_working_exp = models.CharField(max_length=20, blank=True, null=True, choices=YEAR_EXP)
    request_teacher_teaching_exp = models.CharField(max_length=20, blank=True, null=True, choices=YEAR_EXP)
    note = models.TextField(null=True, blank=True)


class Post(models.Model):
    post_detail = models.OneToOneField(PostDetail, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(CustomUser, null=True, blank=True, related_name="teachers")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    range_times = models.ManyToManyField(RangeTime)
    approve_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_user")

    updated_date = models.DateTimeField(null=True, blank=True)
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

