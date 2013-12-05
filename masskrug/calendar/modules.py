from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from ..core import module_manager, Module, ModuleView, Menu
from .models import Calendar, Place

class CalendarView(ModuleView):
  name = 'CalendarView'
  description = _('Display an interactive calendar')
  template_name = 'calendar/calendar_view.html'

  def get_context_data(self, request, content_object=None):
    return {
      'calendar': Calendar.objects.get(),    
    }

  class Meta:
    stylesheets = {
      'fullcalendar/fullcalendar.css', 
      'fullcalendar/fullcalendar.print.css',
    }

    javascript = {
      'lib/jquery.min.js',
      'lib/jquery-ui.custom.min.js',
      'fullcalendar/fullcalendar.min.js',
      'calendar.js',
    }

class CalendarMenu(Menu):
  place = 'navbar'

  title = _('Calendar')

  def items(self):
    items = []
    items.append({
      'title': _('Main'),
      'url': reverse('module-calendar'),
    })

    items.append({
      'header': _('Plannings'),
    })

    for place in Place.objects.filter(planning=True):
      items.append({
        'title': place,
        'url': reverse('module-calendar-planning', kwargs={
          'slug': place.slug,
        }),
      })

    return items

class CalendarModule(Module):
  name = _('Calendar')
  description = _('An application providing an easy-to-use interface to create calendar')

  settings = {
    'url_options': 'module-calendar-options', 
  }

  views = {
    'calendar_view': CalendarView(),
  }

  menus = {
    'calendar_nav': CalendarMenu(), 
  }



module_manager.register(CalendarModule)
