from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from apps.common.models import TimeStampedModel, Tag
from apps.users.models import CustomUser


# Create your models here.
class Post(TimeStampedModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='posts',
        verbose_name=_("user"),
    )
    description = RichTextField()

    def __str__(self):
        return f"{self.user.username} | {self.description[:16]}..."


class PostTag(TimeStampedModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_posts', verbose_name=_("tag"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags', verbose_name=_("tag"))

    def __str__(self):
        return f"{self.tag.name} | {self.post}"
