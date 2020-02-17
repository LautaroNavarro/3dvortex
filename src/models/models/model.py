import boto3
from botocore.client import Config
from enum import IntEnum
from django.db import models
from helpers.date_helpers import get_current_utc_datetime
from django.conf import settings
from users.models.user import User
from image_medias.models.image_media import ImageMedia
from model_medias.models.model_media import ModelMedia
from models.utils import STLUtils
import stl
from stl import mesh


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
    volume = models.CharField(max_length=255)
    max_x = models.CharField(max_length=255)
    max_z = models.CharField(max_length=255)
    max_y = models.CharField(max_length=255)
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

    file_downloaded = False

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
            'volume': str(self.volume),
            'max_x': str(self.max_x),
            'max_y': str(self.max_y),
            'max_z': str(self.max_z),
            'image_media': image_media,
            'privacy': self.privacy,
            'category': self.category_id,
        }

    def get_file_path(self):
        return '{}/{}.stl'.format(
            settings.VOLATILE_FILES_PATH,
            self.model_media_id,
        )

    def download_file(self):

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AMAZON_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AMAZON_ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )

        s3.download_file(
            settings.MODELS_BUCKET_NAME,
            '{}.stl'.format(self.model_media_id),
            self.get_file_path(),
        )
        self.file_downloaded = True

    def get_dimensions_in_mm(self):
        def find_mins_maxs(obj):
            minx = maxx = miny = maxy = minz = maxz = None
            for p in obj.points:
                if minx is None:
                    minx = p[stl.Dimension.X]
                    maxx = p[stl.Dimension.X]
                    miny = p[stl.Dimension.Y]
                    maxy = p[stl.Dimension.Y]
                    minz = p[stl.Dimension.Z]
                    maxz = p[stl.Dimension.Z]
                else:
                    maxx = max(p[stl.Dimension.X], maxx)
                    minx = min(p[stl.Dimension.X], minx)
                    maxy = max(p[stl.Dimension.Y], maxy)
                    miny = min(p[stl.Dimension.Y], miny)
                    maxz = max(p[stl.Dimension.Z], maxz)
                    minz = min(p[stl.Dimension.Z], minz)
            return minx, maxx, miny, maxy, minz, maxz

        if not self.file_downloaded:
            self.download_file()

        main_body = mesh.Mesh.from_file(self.get_file_path())

        minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
        return {
            'x': maxx - minx,
            'y': maxy - miny,
            'z': maxz - minz,
        }

    def get_volume(self):
        stl_utils = STLUtils()

        if not self.file_downloaded:
            self.download_file()

        return stl_utils.calculate_volume(self.get_file_path())

    def calculate_price(self, material_price_per_kilogram, scale=1):
        return "{0:.2f}".format(float(self.volume) * float(material_price_per_kilogram) * 0.0032 * float(scale))
