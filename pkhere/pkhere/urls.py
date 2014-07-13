from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('football.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^bf/$', 'details'),
    #url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
