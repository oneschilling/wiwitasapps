from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wiwitasapps.views.home', name='home'),
    # url(r'^wiwitasapps/', include('wiwitasapps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/', include('courses.urls')),
    url(r'^accounts/', include('wiwitasprofile.urls')),
    url(r'^accounts/', include('registration.urls')),
)
