from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated
class IsAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS and
            request.user and
            is_authenticated(request.user)
        )