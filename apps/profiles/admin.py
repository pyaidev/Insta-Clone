from django.contrib import admin

from apps.profiles.models import Profile, Follower

admin.site.register(Profile)
admin.site.register(Follower)
