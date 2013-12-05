
from .models import Group
from . import module_manager

def groups(request):
  return {
    'groups': Group.objects.filter(hidden=False),
  }


def menus(request):
  menus = {
    'navbar': [],
  }
  for key, module in module_manager.modules.items():
    for key, menu in module.menus.items():
      if menu.place == 'navbar':
        menus['navbar'].append(menu)
        print menu.items()

  return {
    'menus': menus,
  }

