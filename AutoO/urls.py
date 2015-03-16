#from django.conf.urls import patterns, include, url
from django.conf.urls import *

#from django.contrib import admin
#admin.autodiscover()
#from AutoO.views import USER_LOGIN, USER_LOGOUT, display_meta 

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',),
)

urlpatterns += patterns('common.views',
    # Examples:
    # url(r'^$', 'AutoO.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
    url(r'^$', 'USER_LOGIN'),
    url(r'^logout/$', 'USER_LOGOUT'),
    url(r'^chgpass/$', 'USER_CHGPASS'),
    
    url(r'^sys/(?P<module>.*)/(?P<action>.*)$', 'sys'),
)

urlpatterns += patterns('AutoO.views',
    url(r'^admin/$', 'admin'),
    url(r'^admin/\d$','admin_display'),
    url(r'^admin/(?P<module>.*)/(?P<action>.*)$', 'admin'),
    url(r'^server/$', 'server'),
    url(r'^test/$', 'module_test'),
)