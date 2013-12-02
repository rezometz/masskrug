from django.conf.urls import patterns, include, url

from django.views import generic

from .models import Group

urlpatterns = patterns('',

  # Group list
  url(r'^groups$',
    generic.ListView.as_view(model=Group),
    name="group-list",
  ),

)
