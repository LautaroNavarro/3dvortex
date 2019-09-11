import uuid
from django.db import models
from users.models.user import User


class Confirmation(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField()
    changed = models.DateTimeField()
