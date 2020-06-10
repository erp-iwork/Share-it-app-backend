from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from it.models import User
from django.core.exceptions import ValidationError


def get_token(request):
    PREFIX = "Bearer"
    header = request.headers.get("Authorization")
    if header is None:
        return False
    else:
        try:
            bearer, _, token = header.partition(" ")
            if bearer != PREFIX:
                return False
            elif not token:
                return False
            else:
                user = Token.objects.get(key=token)
                return token
        except:
            return False


def get_role(token):
    role = Token.objects.get(key=token).user.roles
    return role


def get_claim(token):
    claim = Token.objects.get(key=token).user.claim
    return claim


def is_superuser(token):
    is_superuser = Token.objects.get(key=token).user.is_superuser
    return is_superuser


def is_admin(token):
    is_admin = Token.objects.get(key=token).user.is_admin
    return is_admin


def get_department(token):
    role = Token.objects.get(key=token).user.department
    return role
