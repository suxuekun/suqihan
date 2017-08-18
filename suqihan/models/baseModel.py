from django.db import models

from ..utils import toStruct
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save
import posixpath
from suqihan.utils.files import moveModelFileToTrash
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation
from django.contrib.contenttypes.models import ContentType


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
        
class DefaultEmptyMixin(models.Field):
    def __init__(self,*args,**kwargs):
        kwargs['default'] = kwargs.get('default') or ""
        super(DefaultEmptyMixin, self).__init__(*args, **kwargs) 
        
class FieldNullAbleMixin(models.Field):
    def __init__(self,*args,**kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super(FieldNullAbleMixin, self).__init__(*args, **kwargs)
        
class Length255Mixin(models.Field):
    def __init__(self,*args,**kwargs):
        kwargs['max_length'] = kwargs.get('max_length') or 255
        super(Length255Mixin, self).__init__(*args, **kwargs)
        
class InputField(models.CharField,FieldNullAbleMixin,DefaultEmptyMixin,Length255Mixin):
    def __init__(self,*args,**kwargs):
        super(InputField, self).__init__(*args, **kwargs)
    pass
        
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
    date = models.DateField()
    class Meta:
        abstract = True
        
class DateTimeMixin(models.Model):
    date = models.DateTimeField()
    class Meta:
        abstract = True
        
class CreatedTimeMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        abstract = True
        
class BaseModel(models.Model):
    def toStruct(self):
        return toStruct(self);
    class Meta:
        abstract = True
        
class ModifyByMixin(models.Model):
    modified_by = models.ForeignKey('UserInfo',default=None,null=True,blank=True)
    class Meta:
        abstract = True
        
def _get_upload_dir(instance,filename):
    dirname = instance.upload_dir;
    filename = posixpath.join(dirname, filename)
    return filename;
        
@receiver(pre_save)
def _on_Doc_Change(sender,instance,**kwargs):
    if (not issubclass(sender,BaseAttachment)):
        return
    instance.size = instance.file.size
    if instance.file and (instance.name == None or instance.name == ""):
        instance.name = instance.file.name
#         print 'auto save doc name:',instance.name,' | doc size:',instance.size
        
class BaseAttachment(BaseModel, TimeStampMixin, ActiveMixin,ModifyByMixin):
    upload_dir = "upload/"
    name = models.CharField(max_length=200,null=True,blank=True,default="");
    size = models.CharField(max_length=50,null=True,blank=True,default="");
    file = models.FileField(upload_to=_get_upload_dir,max_length=500, default="")
    def delete(self, *args, **kwargs):
        moveModelFileToTrash(self.file);
        return super(BaseAttachment, self).delete(*args, **kwargs)
    class Meta:
        abstract = True
        
class GenericAttachment(BaseAttachment):
    master_type = models.ForeignKey(ContentType,db_index = True,null=True,blank=True);
    master_id = models.PositiveIntegerField(null=True,blank=True)
    master = GenericForeignKey('master_type', 'master_id')
    
class AttachementMixin(BaseModel):
    attachments = GenericRelation(GenericAttachment,object_id_field="master_id",content_type_field="master_type");
    class Meta:
        abstract = True
    
class BasePost(BaseModel,TimeStampMixin):
    user = models.ForeignKey('UserInfo',default=None,null=True,blank=True)
    message = models.TextField(default="")
    class Meta:
        abstract = True
        
class PostWithAttach(BasePost,AttachementMixin):
    class Meta:
        abstract = True