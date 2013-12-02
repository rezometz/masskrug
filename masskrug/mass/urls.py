from django.conf.urls import patterns, include, url

from django.views import generic

urlpatterns = patterns('',

  # Index
  url(r'^$',
    generic.TemplateView.as_view(template_name='mass/home.html'),
    name="home",
  ),

)
