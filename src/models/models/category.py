from django.db import models
from helpers.date_helpers import get_current_utc_datetime


class Category(models.Model):

    name = models.CharField(max_length=255)
    father_category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'father_category_id': self.father_category.id if self.father_category else None,
        }
