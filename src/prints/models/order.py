import hashlib
from enum import IntEnum
from django.db import models
from django.conf import settings
from helpers.date_helpers import get_current_utc_datetime
from models.models.model import Model
from prints.models.material import Material
from users.models.user import User
from addresses.models.address import Address
from printers.models.printer import Printer


class Order(models.Model):

    class Status(IntEnum):
        NOT_READY_TO_BE_PRINTED = 0
        READY_TO_BE_PRINTED = 1
        PRITING = 2
        READY_TO_BE_DELIVERED = 3
        DELIVERED = 4

    class PaymentStatus(IntEnum):
        NOT_PAID = 0
        PAID = 1

    address = models.ForeignKey(Address, models.deletion.SET_NULL, null=True)
    preference_id = models.CharField(max_length=255, null=True)
    status = models.IntegerField()
    payment_status = models.IntegerField()
    price = models.CharField(max_length=255)
    user = models.ForeignKey(User, models.deletion.SET_NULL, null=True)
    printer = models.ForeignKey(Printer, models.deletion.SET_NULL, null=True)

    # Needed for printing
    material = models.ForeignKey(Material, models.deletion.SET_NULL, null=True)
    model = models.ForeignKey(Model, models.deletion.SET_NULL, null=True)
    scale = models.CharField(max_length=255)

    changed = models.DateTimeField(default=get_current_utc_datetime)
    created = models.DateTimeField(default=get_current_utc_datetime)

    @property
    def hash(self):
        return hashlib.sha1(
            "{}.{}.{}".format(
                self.id,
                self.user_id,
                settings.SECRET_KEY
            ).encode("UTF-8")).hexdigest()[:5]

    @property
    def serialized(self):
        return {
            'id': self.id,
            'preference_id': self.preference_id,
            'status': self.status,
            'payment_status': self.payment_status,
            'price': self.price,
            'address': self.address.serialized if self.address else None,
            'user': self.user.serialized,
            'printer': self.printer.serialized,
            'material': self.material.serialized,
            'model': self.model.serialized,
            'scale': self.scale,
            'hash': self.hash,
        }
