from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import check_password
from .models import Employee

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            superuser = AuthUser.objects.get(username=username)
            if superuser.check_password(password):
                return superuser
        except AuthUser.DoesNotExist:
            pass
        try:
            regular_user = Employee.objects.get(email=username)
            if regular_user.check_password(password):
                return regular_user
        except Employee.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return AuthUser.objects.get(pk=user_id)
        except AuthUser.DoesNotExist:
            pass
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None