from django.db import models
from django.contrib.auth.models import User, UserManager

import uuid

class UserData(User):
    confirmation = models.CharField(max_length=32)

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.confirmation = uuid.uuid4().hex
        super(UserData, self).save(*args, **kwargs)