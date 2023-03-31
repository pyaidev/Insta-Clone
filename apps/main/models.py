from django.db import models
from django.db.models import FileField, ForeignKey, CASCADE

from apps.common.models import TimeStampedModel


class Story(TimeStampedModel):
    file = FileField(upload_to='stories/')
    author = ForeignKey('users.User', CASCADE)

    def __str__(self):
        return self.author.email

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = 'Story'
