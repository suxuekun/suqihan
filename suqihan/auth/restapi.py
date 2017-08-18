from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from suqihan.api import Version0
from suqihan.auth.viewset import MyUserInfoViewSet

from .viewset import UserViewSet, UserInfoViewSet


router = DefaultRouter()
router.register("user", UserViewSet,'user')
router.register("userinfo", UserInfoViewSet,'userinfo')

myrouter = DefaultRouter()
myrouter.register("userinfo", MyUserInfoViewSet,'userinfo')

me = [
    url(r'^me/',include(myrouter.urls))
    ]

v0 = [
    url(r'^',include(router.urls)),
    url(r'^',include(me))
    ]

apis = [
    url(r'^'+Version0+"/",include(v0))
    ]