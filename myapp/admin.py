from django.contrib import admin
from .models import UserDetail, Post, Tag, Comment, Like, Bookmark
# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)
