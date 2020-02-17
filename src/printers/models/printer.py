from django.db import models
from helpers.date_helpers import get_current_utc_datetime
from addresses.models.address import Address
from enum import IntEnum
from prints.models.material import Material


class Printer(models.Model):

    class Status(IntEnum):
        AVAILABLE = 0
        BUSY = 1
        WAITING_TECHNICAL = 2

    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    model = models.CharField(max_length=255, default='Creality Ender 3')
    # these dimensions are in mm
    max_x = models.CharField(max_length=255, default='220')
    max_y = models.CharField(max_length=255, default='220')
    max_z = models.CharField(max_length=255, default='250')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=Status.AVAILABLE.value)
    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address.serialized if self.address else None,
            'status': self.status,
            'model': self.model,
            'material': self.material.serialized if self.material else None,
            'max_x': self.max_x,
            'max_y': self.max_y,
            'max_z': self.max_z,
        }
