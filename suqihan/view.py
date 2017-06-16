from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from . import utils

class GeneralResponseWrapper(object):
    def __init__(self,code =0 ,result = {}):
        self.code=code
        self.result=result
    def toJSON(self):
        return utils.toJSON(self.__dict__);
    
class loginView(TemplateView):
    template_name = "app/login.html",
    def post(self,request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(GeneralResponseWrapper().toJSON())
        else:
            return HttpResponse(GeneralResponseWrapper(1).toJSON())
        
@method_decorator(never_cache, name='dispatch')
class IndexView(TemplateView):
    template_name = "app/index.html"
