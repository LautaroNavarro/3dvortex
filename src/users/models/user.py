import re
import binascii
import hashlib
import jwt
from django.conf import settings
from enum import IntEnum
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from helpers.date_helpers import get_current_utc_datetime
from helpers.string_helpers import get_random_string
from addresses.models.address import Address


class User(models.Model):

    class Status(IntEnum):
        NOT_CONFIRMED_STATUS = 0
        CONFIRMED_STATUS = 1

    class Type(IntEnum):
        COMMON_USER_TYPE = 0
        ADMIN_USER_TYPE = 1
        PRINTER_USER_TYPE = 2

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    lastname = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=Status.NOT_CONFIRMED_STATUS.value)
    access_level = models.IntegerField(default=Type.COMMON_USER_TYPE.value)
    mercado_pago_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    addresses = models.ManyToManyField(Address, blank=True)
    created = models.DateTimeField(default=get_current_utc_datetime)
    changed = models.DateTimeField(default=get_current_utc_datetime)

    @staticmethod
    def hash_password(password):
        salt = hashlib.sha256(
            get_random_string(12).encode('utf-8')
        ).hexdigest().encode('utf-8')
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,
        )
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('utf-8')

    def set_password(self, password):
        self.password = self.hash_password(password)
        return self.password

    def check_password(self, password_to_check):
        salt = self.password[:64]
        password = self.password[64:]
        password_to_check = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'),
            salt.encode('utf-8'),
            100000,
        )
        password_to_check = binascii.hexlify(password_to_check).decode('utf-8')
        return password_to_check == password

    @property
    def jwt(self):
        paylaod = {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
            'access_level': self.access_level,
        }
        return jwt.encode(paylaod, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

    @staticmethod
    def get_payload_from_jwt(provided_jwt):
        return jwt.decode(provided_jwt, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def validate_password(password):
        if len(password) >= 8:
            if not password.isupper():
                if not password.islower():
                    if re.search('[0-9]', password) is not None:
                        if re.search('\W', password) is not None:
                            return True
        return False

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
            'access_level': self.access_level,
            'status': self.status,
        }
