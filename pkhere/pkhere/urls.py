from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('football.views',
    url(r'^$', 'index'),
    url(r'^score/$', 'score'),
    #url(r'^blog/', include('blog.urls')),
    url(r'^zhibo/$', 'zhibo'),
    url(r'^zhiboDetails/$', 'zhiboDetails'),
)
