from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from apps.common.models import TimeStampedModel, Tag
from apps.users.models import User
from apps.posts.choices import MediaTypes


# Create your models here.
class Post(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name=_("user"),
    )
    text = RichTextField()
    allow_commentary = models.BooleanField(default=True, verbose_name=_("allow commentary"))

    def __str__(self):
        return f"{self.user.username} | {self.text[:32]}..."

    @property
    def likes_count(self):
        likes_number = PostLike.objects.filter(post_id=self.id).count()
        return likes_number

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_medias')
    file = models.FileField(upload_to='posts/%Y/%m/%d/')
    media_type = models.CharField(max_length=3, choices=MediaTypes.choices, default=MediaTypes.IMAGE)

    class Meta:
        verbose_name = 'PostMedia'
        verbose_name_plural = 'PostMedia'

    def __str__(self):
        return f"{self.media_type} | {self.post}"


class Comment(TimeStampedModel):
    user = models.ForeignKey('users.User', models.CASCADE)
    post = models.ForeignKey(
        'posts.Post', models.CASCADE, related_name='comments',
        limit_choices_to={'allow_commentary': True}
    )
    parent = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, related_name='replies')
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:20]}..."

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class PostLike(TimeStampedModel):
    user = models.ForeignKey('users.User', models.CASCADE, related_name='likes')
    post = models.ForeignKey('posts.Post', models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user} | {self.post}"

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
