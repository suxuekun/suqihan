from django.contrib.auth.models import User

from suqihan.models.baseSerializer import getDefaultSerializer

from .models import UserInfo


class UserSerializer(getDefaultSerializer(User)):
    class Meta:
        model = User
        fields = ('id','username','is_staff','first_name','last_name','email','is_active')
        
class UserInfoSerializer(getDefaultSerializer(UserInfo)):
    user = UserSerializer(read_only=True)
        