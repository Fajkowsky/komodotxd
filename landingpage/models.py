from django.db import models
from django.contrib.auth.models import User, UserManager

import uuid
from random import randint

class UserData(User):
    confirmation = models.CharField(max_length=32)
    userID = models.BigIntegerField(null=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.confirmation = uuid.uuid4().hex
        super(UserData, self).save(*args, **kwargs)

    def generate_auth(self):
        if not self.is_active:
            self.userID = int(''.join(["%s" % randint(0, 9) for num in range(0, 10)]))
            password = uuid.uuid4().hex[:6]
            self.set_password(password)
            self.is_active = True
            return password
