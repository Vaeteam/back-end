from constant.choice import STATE, SEX, TEACHING_LOCATION, TEACHING_TIME_UNIT, EDUCATION, YEAR_EXP
from django.db import models
from django.utils import timezone
from user.models import CustomUser
from common.models import AdministrativeUnits, Subject, RangeTime


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
    request_teacher_sex = models.CharField(max_length=6, choices=SEX)
    request_teacher_year_old_from = models.PositiveIntegerField(blank=True, null=True)
    request_teacher_year_old_to = models.PositiveIntegerField(blank=True, null=True)
    request_teacher_education = models.CharField(max_length=20, blank=True, null=True, choices=EDUCATION)
    request_teacher_working_exp = models.CharField(max_length=20, blank=True, null=True, choices=YEAR_EXP)
    request_teacher_teaching_exp = models.CharField(max_length=20, blank=True, null=True, choices=YEAR_EXP)
    note = models.TextField(null=True, blank=True)


class PostStatus(models.Model):
    state = models.CharField(max_length=100, choices=STATE, default=STATE[0][0])
    note = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    selected_teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)


class Post(models.Model):
    last_update_time = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    post_detail = models.OneToOneField(PostDetail, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(CustomUser, null=True, blank=True, related_name="teachers")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    teaching_province = models.ForeignKey(AdministrativeUnits, null=True, blank=True, on_delete=models.CASCADE, related_name="teaching_province")
    teaching_district = models.ForeignKey(AdministrativeUnits, null=True, blank=True, on_delete=models.CASCADE, related_name="teaching_district")
    teaching_ward = models.ForeignKey(AdministrativeUnits, null=True, blank=True, on_delete=models.CASCADE, related_name="teaching_ward")
    subjects = models.ManyToManyField(Subject)
    range_times = models.ManyToManyField(RangeTime)
    approve_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="approve_user")

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
