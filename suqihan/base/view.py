from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http.response import HttpResponse, HttpResponseRedirect
from ..view import GeneralResponseWrapper
from __builtin__ import NotImplementedError
class GeneralCustomAPIView(APIView):
    pass

class CustomAPIViewAuthOnly(GeneralCustomAPIView):
    permission_classes = (IsAuthenticated,)

class SimpleServiceAPI(CustomAPIViewAuthOnly):
    def getService(self):
        raise NotImplementedError('must implement a service')
    
class redirectAPI(APIView):
    def getRedirect(self):
        return None;

class callFuncAPI(APIView):
    def getResultHandler(self):
        raise NotImplementedError('must implement a result handler')
    
class PostHandleResultAPI(SimpleServiceAPI,callFuncAPI):
    @transaction.atomic
    def post(self,request, *args, **kwargs):
        service = self.getService();
        handler = self.getResultHandler()
        struct = request
        result = service(struct)
        
        if result:
            return handler(result)
        else:
            return handler(result)
    
    
class PostRedirectAPI(SimpleServiceAPI,redirectAPI):
    @transaction.atomic
    def post(self,request, *args, **kwargs):
        struct = request
        result = self.getService()(struct)
        if result:
            return HttpResponseRedirect(self.getRedirect())
        else:
            return HttpResponseRedirect(self.getRedirect(),result)
            
class PostSimpleServiceAPI(SimpleServiceAPI):
    @transaction.atomic
    def post(self,request, *args, **kwargs):
        struct = request
        result = self.getService()(struct)
        if result:
            return HttpResponse(GeneralResponseWrapper(result=result).toJSON());
        else:
            return HttpResponse(GeneralResponseWrapper(code=1,result=result).toJSON());