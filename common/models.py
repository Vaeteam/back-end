from django.db import models
from django.utils import timezone
from constant.choice import ADMINISTRATIVE_UNITS, DAY_CHOICE


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True)
    parent_subject = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class RangeTime(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    weekday = models.CharField(choices=DAY_CHOICE, max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"day: {self.weekday}, begin_time:{self.start_time}, end_time: {self.end_time}"



class AdministrativeUnits(models.Model):
    name = models.CharField(max_length=50)
    codename = models.CharField(max_length=50)
    code = models.IntegerField()
    division_type = models.CharField(max_length=50)
    root = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
