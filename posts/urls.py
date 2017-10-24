from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post, name='post'),
    url(r'^post/(?P<post_id>[0-9]+)/post_commentaries$', views.post_commentaries, name='post_commentaries'),
    url(r'^post/(?P<post_id>[0-9]+)/send_commentary$', views.send_commentary, name='send_commentary'),
    url(r'^search/$', views.search, name='search'),
    url(r'^commentary/(?P<commentary_id>[0-9]+)/$', views.commentary, name='commentary'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]