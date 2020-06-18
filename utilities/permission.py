from rest_framework import permissions
from rest_framework.authtoken.models import Token

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class AdminPermissionsAll(permissions.BasePermission):
    """Admin permission not implemented yet """

    def has_permission(self, request, view):
        token = get_token(request)
        if not token:
            return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """The request is authenticated as a user, or is a read-only request."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )
