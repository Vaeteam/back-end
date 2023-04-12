from django.contrib import admin

from .models import Post, PostReview, RangeTime, Subject


# array = [Post, PostReview, Subject, RangeTime]
# admin.site.register(array)

# @admin.register(Post)
# class PostDisplay(admin.ModelAdmin):
#     list_display = (
#         'id', 'author', 'teacher')
#     search_fields = ('id', 'author', 'teacher')


@admin.register(PostReview)
class PostReviewDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'comment', 'score', 't_create', 'is_edited',)
    search_fields = ('id', 'post', 'comment', 'score', 't_create', 'is_edited',)


@admin.register(RangeTime)
class RangeTimeDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'user', 'day', 't_begin', 't_end', 't_create')
    search_fields = ('id', 'post', 'user', 'day', 't_begin', 't_end')


@admin.register(Subject)
class SubjectDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'parent_subject',)
    search_fields = ('id', 'name', 'parent_subject')