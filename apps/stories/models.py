from django.db import models

from apps.common.models import TimeStampedModel
from apps.posts.choices import MediaTypes
from apps.profiles.models import Profile
from apps.users.models import User


class Story(TimeStampedModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Story"


class StoryContent(TimeStampedModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    file = models.FileField(upload_to="story/%Y/%m/%d/")
    type = models.CharField(max_length=6, choices=MediaTypes.choices, default=MediaTypes.IMAGE)

    def __str__(self):
        return str(self.story.id)

    class Meta:
        verbose_name = "ContentStory"
        verbose_name_plural = "ContentStory"


class StoryViewed(TimeStampedModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='viewed_stories')

    def __str__(self):
        return f'{str(self.id)}'

    class Meta:
        verbose_name = "Viewed Story"
        verbose_name_plural = "Viewed Story"
