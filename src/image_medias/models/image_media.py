import boto3
from botocore.client import Config
from django.conf import settings
from django.db import models
from users.models.user import User
from helpers.date_helpers import get_current_utc_datetime


class ImageMedia(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    def upload_image(self, data):
        s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AMAZON_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AMAZON_ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        s3.Bucket(settings.IMAGES_BUCKET_NAME).put_object(Key='{}.png'.format(self.id), Body=data, ACL='public-read')
        self.url = settings.BASE_AMAZON_URL.format(
            BUCKET_NAME=settings.IMAGES_BUCKET_NAME,
            RESOURCE_NAME='{}.png'.format(self.id),
        )
        self.save()

    @property
    def serialized(self):
        return {
            'id': self.id,
            'owner': self.user.email,
            'url': self.url,
        }
