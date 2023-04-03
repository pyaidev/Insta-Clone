from django.contrib import admin

from .models import PostMedia, Post, PostLike, Comment, PostTag


# Register your models here.
admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(PostTag)
