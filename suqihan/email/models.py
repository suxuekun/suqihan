from django.db import models

from suqihan.models.baseModel import BaseModel, ActiveMixin, TimeStampMixin, \
    InputField
from suqihan.utils.strings import multiReplace


class EmailTemplate(BaseModel,ActiveMixin,TimeStampMixin):
    name = InputField()
    title = InputField()
    type = InputField()
    template = models.TextField(default="",null=True,blank=True)
    is_html = models.BooleanField(default = False);
    def feed(self,struct,missing="",badvalue=""):
        title = multiReplace(self.title,struct,missing,badvalue)
        content = multiReplace(self.template,struct,missing,badvalue)
        return {'title':title,'content':content}