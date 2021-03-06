from django.conf.urls import patterns, include, url
from django.contrib import admin

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_id>\d+)/$', views.category_view, name='category'),
    url(r'^topic/(?P<topic_id>\d+)/$', views.topic_view, name='topic'),
    url(r'^(?P<content_type>\w+)/(?P<content_id>\d+)/new/$',
        views.new_content_view, name='new_content'),
    url(r'^search/$', views.search_view, name='search'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^profile/change$', views.profile_change_view, name='profile_change'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^profile/(?P<username>\w+)/$', views.profile_view, name='profile'),
)
