from datetime import datetime


from django.views import generic
from django.views.generic import DetailView, ListView
from django.views.generic.list import BaseListView
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .mixins import JSONResponseMixin
from .models import Event, Calendar, Place

colors = [
  '5BB75B',
  '49AFCD',
  'F5A932',
  'DA4F49',
  'FF0D00',
  'FF9000',
  '009500',
  '00FF1F',
  '004DFF',
  '64OOFF',
  'FFE400',
  'FFAA00',
]

class MainCalendarView(ListView):
  model = Calendar
  context_object_name = 'calendars'

class CalendarView(DetailView):
  model = Calendar
  context_object_name = 'calendar'

class PlaceCalendarView(DetailView):
  model = Place
  slug_url_kwarg = 'place_slug'
  context_object_name = 'place'

class EventListView(ListView):
  model = Event

from pytz import timezone, utc
from django.conf import settings
import icalendar
from django.http import HttpResponse
 
TZ = timezone(settings.TIME_ZONE)
 
def utcisoformat(date):
    """
    Return a datetime object in ISO 8601 format in UTC, without microseconds
    or time zone offset other than 'Z', e.g. '2011-06-28T00:00:00Z'.
    """
    # Convert datetime to UTC, remove microseconds, remove timezone, convert to string
    return date.astimezone(TZ).replace(tzinfo=None).isoformat()

def get_start_and_end(request):
  start = datetime.fromtimestamp(int(request.POST.get('start')) / 1000)
  end = datetime.fromtimestamp(int(request.POST.get('end')) / 1000)
  
  return (start, end)

def return_event_list_as_fullcalendar(events):
    return [{
      'id': x.pk,
      'title': x.name + ' - ' + x.plainPlaces(),
      'start': x.start.isoformat(),
      'end': x.end.isoformat(),
      'url': None,
      'allDay': False,
      'color': x.agenda.color,
    } for x in events]

def render_icalendar(request):
  output = ""
  cal = icalendar.Calendar()
  cal.add('prodid', '-//rezo/djangocal /NONMSGL v1.0//FR')
  cal.add('version', '2.0')
  for calendar in Calendar.objects.all():
    for agenda in calendar.agendas.all():
      for event in agenda.events.all():
        ev = icalendar.Event()
        ev.add('summary', unicode(event))
        ev.add('dtstart', event.start)
        ev.add('dtend', event.end)
        ev['uid'] = '%d@%d@%d' % (event.pk, agenda.pk, calendar.pk)
        cal.add_component(ev)
  for line in cal.content_lines():
    if line:
      output += line + "\r\n";

  response = HttpResponse(output, mimetype="text/calendar")
  response['Content-Disposition'] = 'attachment; filename=events.ics'
  return response

# Ajax request
class EventListAjaxView(JSONResponseMixin, EventListView):
  context_variable = 'object_list'
  
  def get_queryset(self):
    if not self.request.POST.has_key('start') and not self.request.POST.has_key('end'):
      return False
    (start, end) = get_start_and_end(self.request)
    
    filter = Q(start__gt=start) & Q(end__lt=end)
    if self.kwargs.get('slug', None) is not None:
      filter &= Q(agenda_calendar_slug=self.kwargs['slug'])

    agenda_pks = self.request.POST.get('pks').split(',')

    events = self.model.objects.filter(
      filter, 
      agenda__pk__in=agenda_pks,
    )

    return return_event_list_as_fullcalendar(events)

class PlaceEventListAjaxView(JSONResponseMixin, EventListView):
  place_slug = 'place_slug'

  def dispatch(self, *args, **kwargs):
    return super(JSONResponseMixin, self).dispatch(*args, **kwargs)

  def get_queryset(self):
    (start, end) = get_start_and_end(self.request)

    filter = Q(start__gt=start) & Q(end__lt=end)
    filter &= Q(places__slug=self.kwargs['place_slug'])

    events = self.model.objects.filter(
      filter,
    )
    
    return return_event_list_as_fullcalendar(events)


class EventListICSView(ListView):
  model = Calendar
  template_name = 'calendar/calendar.ics'
  context_object_name = 'calendars'

  def options(self, request, *args, **kwargs):
    response = super(EventListICSView, self).options(request, *args, **kwargs)
    response['Content-Type'] = 'text/calendar'
    return response

class CalendarOptionsView(generic.UpdateView):
  form_class = modelform_factory(Calendar, exclude=('content_type', 'object_id'))

  def get_object(self, *args, **kwargs):
    content_type = ContentType.objects.get(model=self.kwargs['content_type'])
    pk = int(self.kwargs['pk'])
    
    (self.calendar, created) = Calendar.objects.get_or_create(
      content_type=content_type,
      object_id=pk,
    )
    
    return self.calendar

  def get_context_data(self, *args, **kwargs):
    context = super(CalendarOptionsView, self).get_context_data(*args, **kwargs)

    self.calendar.save()
    context['object'] = self.calendar.content_type.get_object_for_this_type(pk=self.calendar.object_id).group
  
    return context

  def get_success_url(self, *args, **kwargs):
    
    messages.success(self.request,
      _("Calendar module options saved."),
    )
    
    return self.request.get_full_path()
