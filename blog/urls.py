from django.conf.urls import url
from . import views
from .views import FacetedSearchView, autocomplete

app_name='blog'
urlpatterns = [
    url(r'^$',views.PostListView.as_view(),name='post_list'),
    url(r'^about/$',views.AboutView.as_view(),name='about'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/user/(?P<pk>[\w-]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^find/', FacetedSearchView.as_view(), name='haystack_search'),
    url(r'^grass-to-grace/$', views.GrassToGraceView.as_view(), name='grass_to_grace'),
    url(r'^post/(?P<slug>[-\w]+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    url(r'^create_subscriber/$', views.SubscribeView.as_view(), name='subscribe'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact_us'),
    url(r'^privacy/$', views.PrivacyView.as_view(), name='privacy_policy'),
    url(r'^terms_of_use/$', views.TermsView.as_view(), name='terms'),#test
   url(r'^activate/$', views.activate, name='activate'),
    url(r'^addview/$', views.increaseView, name='addview'),
    url(r'^newsfeed/$', views.newsfeed.as_view(), name='newsfeed'),
]

