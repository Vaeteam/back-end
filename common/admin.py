from django.contrib import admin
from .models import Subject, RangeTime

# @admin.register(RangeTime)
# class RangeTimeDisplay(admin.ModelAdmin):
#     list_display = (
#         'id', 'post', 'user', 'day', 't_begin', 't_end', 't_create')
#     search_fields = ('id', 'post', 'user', 'day', 't_begin', 't_end')


# @admin.register(Subject)
# class SubjectDisplay(admin.ModelAdmin):
#     list_display = (
#         'id', 'name', 'parent_subject',)
#     search_fields = ('id', 'name', 'parent_subject')