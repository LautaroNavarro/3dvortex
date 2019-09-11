from django.db import models


class User(models.Model):

    NOT_CONFIRMED_STATUS = 0
    CONFIRMED_STATUS = 1

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
    email = models.CharField(max_length=255)
    status = models.IntegerField(default=NOT_CONFIRMED_STATUS)
    password = models.CharField(max_length=255)
    mercado_pago_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    created = models.DateTimeField()
    changed = models.DateTimeField()
