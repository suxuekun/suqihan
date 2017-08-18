from suqihan.base.viewset import BaseViewSet
from suqihan.models.baseSerializer import getDefaultSerializer,\
    GenericAttachmentSerializerWithModifiedBy
from suqihan.models.baseModel import GenericAttachment
autoViewSets = {
}
def Viewsetfactory(m,s,b=BaseViewSet):
    class NewClass(b): 
        queryset = m.objects.all()
        serializer_class = s
    NewClass.__name__ = "%sViewSet" % s.__name__
    return NewClass

def getDefaultViewset(m,s=None):
    serializer= s or getDefaultSerializer(m)
    if (serializer):
        viewSet_cls = autoViewSets[serializer.__name__] = autoViewSets.get(serializer.__name__) or Viewsetfactory(m,serializer);
    else:
        return None;
    return viewSet_cls

getMV = getModelViewset = getDefaultViewset

class AutoRecordModifiedByViewSet(BaseViewSet):
    def perform_create(self, serializer):
        super(AutoRecordModifiedByViewSet,self).perform_create(serializer)
        serializer.instance.modified_by = self.request.user
        serializer.instance.save()
    def perform_update(self, serializer):
        super(AutoRecordModifiedByViewSet,self).perform_update(serializer)
        serializer.instance.modified_by = self.request.user
        serializer.instance.save()
        
class AutoRecordUserViewSet(BaseViewSet):
    def perform_create(self, serializer):
        super(AutoRecordUserViewSet,self).perform_create(serializer)
        serializer.instance.user = self.request.user
        serializer.instance.save();


class BaseGenericAttachmentViewSet(AutoRecordModifiedByViewSet):
    emptyInstance = GenericAttachment()
    queryset = GenericAttachment.objects.all()
    serializer_class = GenericAttachmentSerializerWithModifiedBy
    filter_fields = ("id","name","is_active","master_id","master_type")

class GenericAttachmentViewSet(BaseGenericAttachmentViewSet):
    pass

class BasePostViewSet(AutoRecordUserViewSet):
    pass

class BasePostWithAttachViewSet(BasePostViewSet):
    pass
