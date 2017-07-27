from django.conf.urls import url

from follow import views

urlpatterns = [
    url(r'^$', views.suggestions, name='suggestions'),
    url(r'^following/$', views.followings, name='followings'),
    url(r'^followers/$', views.followers, name='followers'),
    url(r'^follow/(?P<id>[-\w]+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<id>[-\w]+)$', views.unfollow, name='unfollow'),
]
