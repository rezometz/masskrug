from django.db import models
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField


class Place(models.Model):
  """
  Place
  """
  name = models.CharField(
    _('Name'),
    max_length=30,
  )
  slug = models.SlugField(
    _('Slug'),
  )

  def __unicode__(self):
    return self.name

class Calendar(models.Model):
  """
  A calendar is composed of multiples agendas
  """
  name = models.CharField(
    _('Name'),
    max_length=30,
  )
  slug = models.SlugField(
    _('Slug'),
  )

  def __unicode__(self):
    return self.name

class Agenda(models.Model):
  """
  A set of agenda
  """
  name = models.CharField(
    _('Name'),
    max_length=40,
  )
  slug = models.SlugField(
    _('Slug'),
  )
  description = models.TextField(
    _('Description'),
    blank=True,
  )
  calendar = models.ForeignKey(
    Calendar,
    related_name="agendas",
  )
  color = RGBColorField(_('Color'))

  def __unicode__(self):
    return '%(calendar)s - %(agenda)s' % {
      'calendar': self.calendar,
      'agenda': self.name,
    }

  class Meta:
    ordering = ('calendar__name', 'name', )

class Event(models.Model):
  """
  An event
  """
  name = models.CharField(
    _('Name'),
    max_length=60,
  )
  start = models.DateTimeField(
    _('Start'),
  )
  end = models.DateTimeField(
    _('End')
  )
  agenda = models.ForeignKey(
    Agenda,
    related_name="events",
  )

  places = models.ManyToManyField(
    Place,
    related_name="events",
  )

  def plainPlaces(self):
    return ', '.join([x.name for x in self.places.all()])

  def __unicode__(self):
    return self.name
