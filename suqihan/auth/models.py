from django.db import models
from django.db.models.aggregates import Sum
from django.contrib.auth.models import User
from ..models.base import BaseModel, TimeStampMixin

class UserInfo(BaseModel, TimeStampMixin):
    user = models.OneToOneField(User, related_name='userinfo')
    user_other_info = models.CharField(default="",max_length=100)

    def __str__(self):
        return self.user.__str__();
    def get_sum(self):
        result = self.user.capitals.all().aggregate(total=Sum('value'))
        print result;
        value = result.get('total');
        print value;
        self.summary = value;
        print self.summary;
        self.save()
    
    