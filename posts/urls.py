from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post, name='post'),
    url(r'^post/(?P<post_id>[0-9]+)/post_commentaries$', views.post_commentaries, name='post_commentaries'),
    url(r'^post/(?P<post_id>[0-9]+)/send_commentary$', views.send_commentary, name='send_commentary'),
    url(r'^commentary/(?P<commentary_id>[0-9]+)/$', views.commentary, name='commentary'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]