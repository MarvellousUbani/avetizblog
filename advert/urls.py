from django.conf.urls import url
from . import views

app_name="advert"
urlpatterns = [
     url(r'^$', views.Dashboard.as_view(), name='dashboard'),
     url(r'^post/(?P<pk>\d+)/edit/$', views.postUpdate.as_view(), name='update_post'),
     url(r'^create_post/$', views.createPost.as_view(), name='create_post'),
     url(r'^manage_posts/$', views.postList.as_view(), name='post_list'),
     url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='delete_post'),
     url(r'^post/(?P<pk>\d+)/submit/$', views.PostSubmitView.as_view(), name='submit_post'),
     url(r'^manage_wallet/$', views.TransactionListView.as_view(), name='transaction_list'),
     url(r'^create_transaction/$', views.TransactionCreateView.as_view(), name='create_transaction'),
     url(r'^advert_list/$', views.AdvertListView.as_view(), name='advert_list'),
     url(r'^create_advert/$', views.createAdvert.as_view(), name='create_advert'),
     url(r'^advert/(?P<pk>\d+)/remove/$', views.AdvertDeleteView.as_view(), name='delete_advert'),
     url(r'^advert/(?P<pk>\d+)/update/$', views.AdvertUpdateView.as_view(), name='update_advert'),
     url(r'^profile/$', views.ProfileUpdateView.as_view(), name='profile'),
     url(r'^approve_payt/$', views.ApprovePaytView.as_view(), name='approve_payt'),
     
]