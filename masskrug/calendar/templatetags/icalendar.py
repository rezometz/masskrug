from django import template


register = template.Library()

def ical_datetime(date):
  return date.strftime('%Y%m%dT%H%M%SZ')
register.filter('ical_datetime', ical_datetime)
