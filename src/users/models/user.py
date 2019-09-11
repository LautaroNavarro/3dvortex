from enum import IntEnum
import binascii
import hashlib
import jwt
from django.db import models
from users.helpers.date_helpers import get_current_utc_datetime
from users.helpers.string_helpers import get_random_string


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
    created = models.DateTimeField(default=get_current_utc_datetime)
    changed = models.DateTimeField(default=get_current_utc_datetime)

    def set_password(self, password):
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
        self.password = (salt + pwdhash).decode('utf-8')
        return self.password

    def check_password(self, password_to_check):
        salt = self.password[:64]
        password = self.password[64:]
        password_to_check = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'),
            salt.encode('ascii'),
            100000,
        )
        password_to_check = binascii.hexlify(password_to_check).decode('ascii')
        return password_to_check == password

    @property
    def jwt(self):
        paylaod = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'access_level': self.access_level,
        }
        return jwt.encode(paylaod, self.password, algorithm='HS256').decode()

    def get_payload_from_jwt(self, jwt):
        return jwt.decode(jwt, self.password, algorithm='HS256')
