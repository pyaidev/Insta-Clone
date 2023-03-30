from django.db import models


class MediaTypes(models.TextChoices):
    VIDEO = 'VID', 'Video'
    IMAGE = 'IMG', 'Image'
