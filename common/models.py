from django.db import models
from django.utils import timezone
from constant.choice import DAY_CHOICE


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True)
    parent_subject = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class RangeTime(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    available_day = models.IntegerField(choices=DAY_CHOICE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"day: {self.day}, begin_time:{self.time_begin}, end_time: {self.time_end}"