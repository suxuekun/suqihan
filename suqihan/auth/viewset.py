from django.contrib.auth.models import User
import django_filters
from django_filters.filters import DateTimeFilter
from rest_framework.compat import is_authenticated

from suqihan.auth.serializer import UserSerializer, UserInfoSerializer

from ..base.viewset import BaseViewSet
from .models import UserInfo


# from . import serializer
# from suqihan.models.baseSerializer import getDefaultSerializer
class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('id','is_active','username')
    search_fields = ('username',)  
    ordering_fields = ('id','lastmodified',)
    
class UserInfoViewSet(BaseViewSet):
    queryset = UserInfo.objects.select_related('user')
    serializer_class = UserInfoSerializer
    filter_fields = ('id','user__is_active',)
    ordering_fields = ('id','lastmodified',)
    
class MyUserInfoViewSet(UserInfoViewSet):
    def get_queryset(self):
        if is_authenticated(self.request.user):
            return super(MyUserInfoViewSet,self).get_queryset().filter(user=self.request.user)
        else:
            return super(MyUserInfoViewSet,self).get_queryset().none()
    
class DateRangeFilter(django_filters.FilterSet):
    max = DateTimeFilter(name='date', lookup_type='lte')
    min = DateTimeFilter(name='date', lookup_type='gte')
