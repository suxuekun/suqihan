from django.contrib.admin.sites import AdminSite
from django.views.decorators.cache import never_cache

from .actions import export_as_xls


class MyAdminSite(AdminSite):
    site_header = "suqihan ADMIN"
    site_title = "suqihan blog"
    @never_cache
    def index(self, request, extra_context=None):
        return super(MyAdminSite,self).index(request,extra_context)
    
site = MyAdminSite(name='suqihan')
site.add_action(export_as_xls)