from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','is_staff','first_name','last_name','email','is_active')
        
class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserInfo
        