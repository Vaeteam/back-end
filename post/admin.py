from django.contrib import admin

from .models import Post, PostReview, RangeTime, Subject


# array = [Post, PostReview, Subject, RangeTime]
# admin.site.register(array)

@admin.register(Post)
class PostDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'content', 'address', 'fee', 'duration', 'note', 'state',
        'active', 't_create', 'date_posted', 'approve_user',)
    search_fields = ('id', 'title', 'author', 'content', 'address', 'fee', 'duration', 'note', 'state',
                     'active', 'date_posted', 'approve_user',)


@admin.register(PostReview)
class PostReviewDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'comment', 'score', 't_create', 'is_edited',)
    search_fields = ('id', 'post', 'comment', 'score', 't_create', 'is_edited',)


@admin.register(RangeTime)
class RangeTimeDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'user', 'day', 'time_begin', 'time_end', 't_create')
    search_fields = ('id', 'post', 'user', 'day', 'time_begin', 'time_end')


@admin.register(Subject)
class SubjectDisplay(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'parent_subject',)
    search_fields = ('id', 'name', 'parent_subject')