from enum import IntEnum
from django.db import models
from helpers.date_helpers import get_current_utc_datetime
from users.models.user import User
from image_medias.models.image_media import ImageMedia
from model_medias.models.model_media import ModelMedia


class Model(models.Model):

    class Privacy(IntEnum):
        PRIVATE = 0
        PUBLIC = 1

        @classmethod
        def all_values(cls):
            return (
                cls.PRIVATE.value,
                cls.PUBLIC.value,
            )

        @classmethod
        def privacy_id_is_valid(cls, privacy_id):
            return (privacy_id in cls.all_values())

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, null=True)
    model_media = models.ForeignKey(
        ModelMedia,
        on_delete=models.CASCADE,
        related_name='model_media',
        default=None,
        null=True,
    )
    volume = models.CharField(max_length=255, null=True)
    image_media = models.ForeignKey(
        ImageMedia,
        on_delete=models.CASCADE,
        related_name='image_model',
        default=None,
        null=True,
    )
    privacy = models.IntegerField()
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    printed_quantity = models.IntegerField(default=0)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def serialized(self):
        model_media = None
        if self.model_media:
            model_media = {
                'id': self.model_media.id,
                'url': self.model_media.url,
            }
        image_media = None
        if self.image_media:
            image_media = {
                'id': self.image_media.id,
                'url': self.image_media.url,
            }
        return {
            'id': self.id,
            'user': self.user.id,
            'name': self.name,
            'description': self.description,
            'model_media': model_media,
            'volume': self.volume,
            'image_media': image_media,
            'privacy': self.privacy,
            'category': self.category_id,
        }
