from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from AutoO.views import USER_LOGIN, add_hours, display_meta 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AutoO.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$','django.views.static.serve',),
    
    url(r'^time/(\d{2})/$', add_hours),
    url(r'^$', USER_LOGIN),
    url(r'^test/$', display_meta),
)
