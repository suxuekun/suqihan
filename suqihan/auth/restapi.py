from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .viewset import UserViewSet, UserInfoViewSet
router = DefaultRouter()
router.register("user", UserViewSet,'user')
router.register("userinfo", UserInfoViewSet,'userinfo')

apis = [
    url(r'^',include(router.urls))
    ]