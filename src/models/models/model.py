from enum import IntEnum
from django.db import models
from helpers.date_helpers import get_current_utc_datetime
from users.models.user import User
from medias.models.media import Media


class Model(models.Model):

    class Privacy(IntEnum):
        PRIVATE = 0
        PUBLIC = 1

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    media_model = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='model_model', default=None)
    volume = models.CharField(max_length=255)
    media_image = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='image_model', default=None)
    privacy = models.IntegerField()
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)
