from django.contrib import admin

from .models import PostMedia, Post


# Register your models here.
admin.site.register(Post)
admin.site.register(PostMedia)
