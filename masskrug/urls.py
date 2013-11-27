from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Main
    url(r'^', include('masskrug.mass.urls')),

    # MassKrug Calendar
    url(r'^calendar/', include('masskrug.calendar.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
