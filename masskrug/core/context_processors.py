
from .models import Group

def groups(request):
  return {
    'groups': Group.objects.filter(hidden=False),
  }
