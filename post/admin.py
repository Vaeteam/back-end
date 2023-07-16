from django.contrib import admin

from .models import Post, PostDetail, PostReview


array = [Post, PostReview, PostDetail]
admin.site.register(array)
