from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from suqihan.api import Version0

from .viewset import ItemViewSet,CalendarEventViewSet


router = DefaultRouter()
router.register("item", ItemViewSet,'item')
router.register("event", CalendarEventViewSet,'event')

me = [
#     url(r'^me/',include(myrouter.urls))
    ]

v0 = [
    url(r'^',include(router.urls)),
    url(r'^',include(me))
    ]

apis = [
    url(r'^'+Version0+"/",include(v0))
    ]