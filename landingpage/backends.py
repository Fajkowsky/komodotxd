from django.contrib.auth.models import check_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser

from models import UserData

# custom backend for email login purposes
class LoginBackend:

    def authenticate(self, userID=None, password=None):
        if userID and password is not None:
            try:
                user = UserData.objects.get(userID=userID)
                if user.check_password(password):
                    user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
                    return user
            except UserData.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return UserData.objects.get(pk=user_id)
        except UserData.DoesNotExist:
            return None


def get_user(userID):
    if not userID:
        return AnonymousUser()
    return LoginBackend().get_user(userID) or AnonymousUser()
