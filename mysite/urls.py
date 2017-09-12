"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.contrib import auth

app_name='blog'

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'', include('blog.urls')),
    url(r'account/', include('account.urls')),
    url(r'^dashboard/', include('advert.urls')),
    url(r'^password_reset/$', auth.views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth.views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth.views.password_reset_complete, name='password_reset_complete'),

    
    #url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    
]
