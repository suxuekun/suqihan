from django.contrib.auth.models import User
import django_filters
from django_filters.filters import DateTimeFilter
from ..base.viewset import BaseViewSet
from .models import UserInfo
from .serializer import UserInfoSerializer, UserSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('id','is_active','username')
    search_fields = ('username',)  
    ordering_fields = ('id','lastmodified',)
    

class UserInfoViewSet(BaseViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    filter_fields = ('id','user__is_active',)
    ordering_fields = ('id','lastmodified',)
    
class DateRangeFilter(django_filters.FilterSet):
    max = DateTimeFilter(name='date', lookup_type='lte')
    min = DateTimeFilter(name='date', lookup_type='gte')
