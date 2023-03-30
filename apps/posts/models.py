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


from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import FileField, ForeignKey, CASCADE, TextField, CharField, BooleanField, SET_NULL, IntegerField, \
    Count, PROTECT


class PostMedia(TimeStampedModel):
    file = FileField(upload_to='posts/')

    class Meta:
        verbose_name = 'PostMedia'
        verbose_name_plural = 'PostMedia'


class Post(BaseModel):
    file = ForeignKey('posts.PostMedia', PROTECT)
    author = ForeignKey('profiles.Profile', CASCADE)
    description = TextField()
    tags = ArrayField(CharField(max_length=255))
    is_comment = BooleanField(default=True)

    def __str__(self):
        return self.description




class Comment(BaseModel):
    user = ForeignKey('profiles.Profile', CASCADE)
    post = ForeignKey('posts.Post', CASCADE, limit_choices_to={'is_comment': True})
    parent = ForeignKey('self', SET_NULL, null=True, blank=True, related_name='replies')
    text = TextField()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'


class Like(BaseModel):
    user = ForeignKey('profiles.Profile', CASCADE)
    post = ForeignKey('posts.Post', CASCADE)

    def __str__(self):
        return self.post.description

    class Meta:
        verbose_name = 'Likes'
        verbose_name_plural = 'Likes'