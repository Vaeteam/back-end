from django.contrib import admin

from .models import Post, PostReview


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
