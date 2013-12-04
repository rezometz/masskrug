from django.utils.translation import ugettext_lazy as _

from ..core import module_manager, Module
from .models import Calendar

class CalendarModule(Module):
  name = _('Calendar')
  description = _('An application providing an easy-to-use interface to create calendar')

  settings = {
    'url_options': 'module-calendar-options', 
  }

module_manager.register(CalendarModule)
