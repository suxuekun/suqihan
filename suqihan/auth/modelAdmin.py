from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ..models.baseModelAdmin import BaseModelAdminDefaultOrdering
from ..actions import import_as_csv
    
from .models import UserInfo

class UserInfoInline(StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'userinfo'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)
    actions = (import_as_csv,)
    
class UserInfoAdmin(BaseModelAdminDefaultOrdering):
    pass


    