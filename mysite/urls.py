from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.contrib import auth
from blog.views import autocomplete
app_name='blog'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
     url(r'^imagefit/', include('imagefit.urls')),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'', include('blog.urls')),
    url(r'^search/autocomplete/$', autocomplete),
    url(r'account/', include('account.urls')),
    url(r'^dashboard/', include('advert.urls')),
    url(r'^password_reset/$', auth.views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth.views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth.views.password_reset_complete, name='password_reset_complete'),
    #url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
   # url(r'^newsletter/', include('newsletter_signup.urls')),
]
