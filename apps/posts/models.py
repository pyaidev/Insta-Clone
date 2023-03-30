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
    tags = models.ArrayField(models.CharField(max_length=255))
    is_comment = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} | {self.description[:16]}..."

    @property
    def likes_count(self):
        like = Like.objects.filter(post_id=self.id).count()
        return like

    @property
    def comments_count(self):
        comment = Comment.objects.filter(post_id=self.id).count()
        return comment

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('post')
        verbose_name_plural = _('posts')


class PostTag(TimeStampedModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_posts', verbose_name=_("tag"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags', verbose_name=_("tag"))

    def __str__(self):
        return f"{self.tag.name} | {self.post}"


class PostMedia(TimeStampedModel):
    file = models.FileField(upload_to='posts/')

    class Meta:
        verbose_name = 'PostMedia'
        verbose_name_plural = 'PostMedia'


class Comment(TimeStampedModel):
    user = models.ForeignKey('profiles.Profile', models.CASCADE)
    post = models.ForeignKey('posts.Post', models.CASCADE, limit_choices_to={'is_comment': True})
    parent = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, related_name='replies')
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:20]}..."

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Like(TimeStampedModel):
    user = models.ForeignKey('profiles.Profile', models.CASCADE, related_name='likes')
    post = models.ForeignKey('posts.Post', models.CASCADE, related_name='likes')

    def __str__(self):
        return self.post.description

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
