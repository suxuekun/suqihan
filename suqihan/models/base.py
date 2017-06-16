from django.db import models
from ..utils import toStruct
class ActiveMixinDefaultFalse(models.Model):
    is_active = models.BooleanField(default=False)
    
    def active(self):
        self.is_active = True
        
    def deactive(self):
        self.is_active = False
        
    class Meta:
        abstract = True

class ActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)
    
    def active(self):
        self.is_active = True
        
    def deactive(self):
        self.is_active = False
        
    class Meta:
        abstract = True
        
class NormalMoneyField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 20
        kwargs['decimal_places'] = 4
        super(NormalMoneyField, self).__init__(*args, **kwargs)
        
class NormalMoneyFieldWithDefault(NormalMoneyField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = "0.0000"
        super(NormalMoneyFieldWithDefault, self).__init__(*args, **kwargs)

class NormalMoneyFieldWithDefaultNullable(NormalMoneyFieldWithDefault):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super(NormalMoneyFieldWithDefaultNullable, self).__init__(*args, **kwargs)  
        
class TimeStampMixin(models.Model):
    lastmodified = models.DateTimeField(auto_now = True,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        abstract = True
        
class DateMixin(models.Model):
    date = models.DateTimeField()
    class Meta:
        abstract = True
        
class CreatedTimeMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        abstract = True
# post_update = Signal()
# 
# class BaseQuerySetTriggerUpdate(models.query.QuerySet):
#     def update(self, **kwargs):
#         old_update = super(BaseQuerySetTriggerUpdate, self).update(**kwargs)
#         post_update.send(sender=self.model)
#         return old_update
# class BaseManagerTriggerUpdate(models.Manager):
#     def getqueryset(self):
#         return BaseQuerySetTriggerUpdate(self.model, using=self._db)
        
class BaseModel(models.Model):
    def toStruct(self):
        return toStruct(self);
    class Meta:
        abstract = True