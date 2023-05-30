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
    available_day = models.CharField(choices=DAY_CHOICE, max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"day: {self.available_day}, begin_time:{self.start_time}, end_time: {self.end_time}"