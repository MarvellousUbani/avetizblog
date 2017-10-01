from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views



app_name='account'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^signup/$', views.SignUp.as_view(), name="signup"),
	#url(r'^password_change/$', views.PasswordChange.as_view(), name="password_change"),
    
]