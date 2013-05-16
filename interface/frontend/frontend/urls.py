from django.conf.urls import patterns, include, url
from frontend.views import hello,current_datetime,hours_ahead,searchgui

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^hello/$',hello),
    url(r'^hello/datum/$',current_datetime),
    url(r'^hello/datum/plus/(\d{1,2})/$',hours_ahead),
#    url(r'^search/$',searchgui),
    url(r'^$',searchgui),
    # Examples:
    # url(r'^$', 'frontend.views.home', name='home'),
    # url(r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
