from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.models import TimeStampedModel


# Create your models here.
class CustomUser(AbstractUser, TimeStampedModel):
    pass
