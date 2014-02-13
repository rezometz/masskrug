from django.conf.urls import patterns, include, url


from .views import EventListAjaxView, CalendarView, MainCalendarView, \
  PlaceCalendarView, PlaceEventListAjaxView, \
  EventListICSView, CalendarOptionsView
from .models import Calendar, Event

urlpatterns = patterns('',
  url(r'^calendar$',
    MainCalendarView.as_view(),
    name="calendar",
  ),

  url(r'^(?P<place_slug>[\w-]+)/planning$',
    PlaceCalendarView.as_view(),
    name="place-schedule"
  ),

  # Ajax place events
  url(r'^(?P<place_slug>[\w-]+)/events/ajax$',
    PlaceEventListAjaxView.as_view(),
    name="place-events-ajax"
  ),


  url(r'^(?P<slug>\w+)$',
    CalendarView.as_view(),
    name="calendar",
  ),

  url(r'^(?P<slug>\w+)/ajax/events$',
    EventListAjaxView.as_view(),
    name="event-list-ajax",
  ),
  url(r'^ajax/events$',
    EventListAjaxView.as_view(),
    name="event-list-ajax",
  ),

  url(r'^events.ics$',
    EventListICSView.as_view(),
    name="event-list-ics",
  ),


  # Module Options
  url(r'^calendar/(?P<content_type>[\w_]+)/(?P<pk>\d+)$',
    CalendarOptionsView.as_view(),
    name="module-calendar-options",
  ),

  # Module Calendar
  url(r'^calendar$',
    MainCalendarView.as_view(),
    name="module-calendar",
  ),

  # Module Planning
  url(r'^(?P<slug>[\w-]+)/planning$',
    PlaceCalendarView.as_view(),
    name="module-calendar-planning",
  ),


)
