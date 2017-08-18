import inspect

from django.db import models
from rest_framework import serializers

from suqihan.utils.strings import getDecentAttrSilent
from suqihan.models.baseModel import GenericAttachment
from suqihan.auth.models import UserInfo
from django.contrib.auth.models import User

class BaseSerializer(serializers.ModelSerializer):
    pass

autoSerializers ={
}
def Serializerfactory(m) :
#     print 'serializer factory for', m
    class NewClass(BaseSerializer): 
        class Meta:
            fields = "__all__"
            model = m
    NewClass.__name__ = "%sSerializer" % m.__name__
    return NewClass

def getDefaultSerializer(model):
    if (inspect.isclass(model) and issubclass(model,models.Model)):
        serializer_cls = autoSerializers[model.__name__] = autoSerializers.get(model.__name__) or Serializerfactory(model);
    else:
        return None;
    return serializer_cls

getMS = getModelSerializer = getDefaultSerializer

class UserSerializerNormal(getMS(User)):
    pass

class UserInfoSerializerNormal(getMS(UserInfo)):
    user = UserSerializerNormal(read_only=True)
    pass

class HistorySerializerDetailMixin(serializers.ModelSerializer):
    modified_by_user = UserInfoSerializerNormal(source="modified_by",read_only=True)

class FlatSerializer(serializers.Serializer):
    flat_inlines=[]
    def to_representation(self, instance):
        ret = super(FlatSerializer,self).to_representation(instance)
        
        for item in self.flat_inlines:
            key = item.get('key');
            serializer_cls = item.get('serializer');
            inline_instance = getDecentAttrSilent(instance,key);
            serializer = serializer_cls(inline_instance, context=self.context)
            inline_ret = serializer.to_representation(inline_instance)
            for inline_key in inline_ret:
                if (ret.get(inline_key) == None):
                    ret[inline_key] = inline_ret[inline_key]
                else:
                    ret[key+ "_" + inline_key] = inline_ret[inline_key]
                
        return ret
        
        

class GenericAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericAttachment
class GenericAttachmentSerializerWithModifiedBy(GenericAttachmentSerializer,HistorySerializerDetailMixin):
    pass

class UserAbleSerializerMixin(object):
    user = UserInfoSerializerNormal(read_only=True)

class WithAttachmentSerializerMixin(object):
    attachments = serializers.PrimaryKeyRelatedField(queryset=GenericAttachment.objects.all(),many=True)
    
class WithAttachementDetailSerializerMixin(object):
    attachmentList = GenericAttachmentSerializer(source="attachments",read_only=True,many=True)
        

