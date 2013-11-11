from django.contrib.auth.models import check_password
from django.contrib.auth.backends import ModelBackend

from models import UserData


class LoginBackend(object):

    def authenticate(self, userID=None, password=None):
        if userID and password is not None:
            try:
                user = UserData.objects.get(userID=userID)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
