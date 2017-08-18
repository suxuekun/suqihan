from django.contrib.auth.models import User
from django.db import models

from suqihan.models.baseModel import BaseModel, TimeStampMixin

class UserInfo(BaseModel, TimeStampMixin):
    user = models.OneToOneField(User, related_name='userinfo')

    def __str__(self):
        return self.user.__str__();
    