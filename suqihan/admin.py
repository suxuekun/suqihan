from .actions import export_as_xls
from django.views.decorators.cache import never_cache
from django.contrib.admin.sites import AdminSite

class MyAdminSite(AdminSite):
    site_header = "dj example ADMIN"
    site_title = "dj example ADMIN"
    @never_cache
    def index(self, request, extra_context=None):
        return super(MyAdminSite,self).index(request,extra_context)
    
site = MyAdminSite(name='dj example ADMIN')
site.add_action(export_as_xls)