"""suqihan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import logout
from django.views.i18n import JavaScriptCatalog

from . import admin, auth ,test
from .view import  IndexView, loginView


apis = []
apis += auth.apis
apis += test.apis

login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/')
urlpatterns = [
    url(r'^login/$',login_forbidden(loginView.as_view(template_name="app/login.html")),name="login"),
    url(r'^logout/$', logout,{'template_name':"app/logout.html"},name="logout"),
    url(r'^$',IndexView.as_view(),name='index'),
    
    url(r'^auth/',include(auth.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/',include(apis)),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]



if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.TEMPLATE_URL, document_root=settings.TEMPLATE_ROOT)
    


