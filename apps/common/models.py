from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True


class Tag(TimeStampedModel):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

