from django.db import models
from helpers.date_helpers import get_current_utc_datetime


class Material(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    # Price in USD
    price_per_kilogram = models.CharField(max_length=255)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)
