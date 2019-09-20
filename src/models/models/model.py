from enum import IntEnum
from django.db import models
from helpers.date_helpers import get_current_utc_datetime
from users.models.user import User
from image_medias.models.image_media import ImageMedia


class Model(models.Model):

    class Privacy(IntEnum):
        PRIVATE = 0
        PUBLIC = 1

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    model_media = models.CharField(max_length=1024)
    volume = models.CharField(max_length=255)
    image_media = models.ForeignKey(ImageMedia, on_delete=models.CASCADE, related_name='image_model', default=None)
    privacy = models.IntegerField()
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)
