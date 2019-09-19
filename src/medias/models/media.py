# import boto3
# from botocore.client import Config
# from django.conf import settings
from enum import IntEnum
from django.db import models
from users.models.user import User
from helpers.date_helpers import get_current_utc_datetime


class Media(models.Model):

    class MediaType(IntEnum):
        IMAGE = 0
        MODEL = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_type = models.IntegerField()
    url = models.CharField(max_length=255)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    # def upload(self, image):
    #     data = open('test.png', 'rb')
    #     s3 = boto3.resource(
    #         's3',
    #         aws_access_key_id=settings.AMAZON_ACCESS_KEY_ID,
    #         aws_secret_access_key=settings.AMAZON_ACCESS_SECRET_KEY,
    #         config=Config(signature_version='s3v4')
    #     )
    #     s3.Bucket(settings.IMAGES_BUCKET_NAME).put_object(Key='{}.png'.format(self.id), Body=data, ACL='public-read')
    #     self.image_url = settings.BASE_AMAZON_URL.format(
    #         BUCKET_NAME=settings.IMAGES_BUCKET_NAME,
    #         RESOURCE_NAME='{}.png'.format(self.id),
    #     )
