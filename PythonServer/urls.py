from django.conf.urls import patterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from server.views import index, sendAll

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PythonServer.views.home', name='home'),
    # url(r'^PythonServer/', include('PythonServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ('^index/$', index),
    ('^sendAll/$', sendAll),
)
