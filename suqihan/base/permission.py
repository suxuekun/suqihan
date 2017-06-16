from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated
from suqihan.base.exceptions import NotAuth

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        res = (
            request.user and
            is_authenticated(request.user)
        )
        if not res:
            raise NotAuth()
        return res


class IsAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        res = (
            request.method in SAFE_METHODS and
            request.user and
            is_authenticated(request.user)
        )
        if not res:
            raise NotAuth()
        return res
            