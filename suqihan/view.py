from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView

from suqihan.base.exceptions import AuthFail
from suqihan.base.response import GeneralResponseWrapper


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
            return HttpResponse(AuthFail().toJson(),status=401)
        
@method_decorator(never_cache, name='dispatch')
class IndexView(TemplateView):
    template_name = "app/index.html"
