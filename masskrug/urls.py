from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    
    # Main
    url(r'^', include('masskrug.mass.urls')),

    # MassKrug Calendar
    url(r'^module/', include('masskrug.calendar.urls')),

    # MassKrug Core
    url(r'^', include('masskrug.core.urls')), 
  
    # Admin
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',
      'django.views.static.serve',
      {
        'document_root': settings.MEDIA_ROOT,
      }
    ),
  )
