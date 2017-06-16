from django.conf.urls import url, include
from django.contrib.auth import views
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin
from .. import admin
from . import restapi
from .view import resetPasswordAPI
from .models import UserInfo
from .modelAdmin import UserAdmin, UserInfoAdmin
from .form import password_reset

# admin.site.unregister(User)
admin.site.register(Group,GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserInfo,UserInfoAdmin)

apis = restapi.apis

urls = [
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^resetPassword/$',resetPasswordAPI.as_view(),name = "reset_password")
    ]