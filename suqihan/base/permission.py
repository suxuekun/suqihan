from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoObjectPermissions

from suqihan.base import error_code
from suqihan.base.exceptions import NotAuth, BaseAPIException, \
    GeneralError
from suqihan.base.response import GeneralResponseWrapper


def add_view_permissions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding a view permission too all our 
    content types.
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "view_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can view %s" % content_type.name)
            print "Added view permission for %s" % content_type.name

# check for all our view permissions after a migrate
post_migrate.connect(add_view_permissions)

class TestPerm(BasePermission):
    def has_permission(self, request, view):
        res = (True)
        return res
    def has_object_permission(self, request, view, obj):
        res = (True)
        return res

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
            request.user and
            (
                (request.method in SAFE_METHODS and
                is_authenticated(request.user))
                or
                request.user.is_superuser
            )
            
            
        )
        if not res:
            raise NotAuth()
        return res
     
class AllCanRead(BasePermission):
    def has_permission(self, request, view):
        res = (
            request.method in SAFE_METHODS
        )
        if not res:
            raise GeneralError()
        return res
    
class AllCanChange(BasePermission):
    def has_permission(self, request, view):
        res = ()
        if not res:
            raise BaseAPIException(GeneralResponseWrapper(code=error_code.ERROR).__dict__)
        return res
    
class AllCanDelete(BasePermission):
    pass

class OwnerCanRead(BasePermission):
    pass

class OwnerCanChange(BasePermission):
    pass

class OwnerCanDelete(BasePermission):
    pass
        
    
class IsAuthenticatedStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        res = (
            request.method in SAFE_METHODS
            or
            (
                request.user and
                is_authenticated(request.user) and
                (request.user.is_staff or request.user.is_superuser)
            )
        )
        if not res:
            raise NotAuth()
        return res

class ModelObjectPerm(DjangoObjectPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    def has_permission(self, request, view):
        res = super(ModelObjectPerm,self).has_permission(request, view)
        if not res:
            raise NotAuth()
        return res
    def has_object_permission(self, request, view, obj):
        res = super(ModelObjectPerm,self).has_object_permission(request, view,obj)
        if not res:
            raise NotAuth()
        return res
        
            