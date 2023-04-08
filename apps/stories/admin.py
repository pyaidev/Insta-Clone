from django.contrib import admin

from apps.stories.models import Story, StoryContent

admin.site.register(Story)
admin.site.register(StoryContent)