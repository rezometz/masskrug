import os, string, importlib

from django.conf import settings
from django.template.defaultfilters import slugify

class ModuleView(object):
  pass

class Menu(object):
  pass

class Module(object):
  name = ''
  
  def slug(self):
    return slugify(self.name)

class ModuleManager(object):
  modules = {}

  def autodiscover(self):
    for app in settings.INSTALLED_APPS:
      name = app + '.modules'
      path = string.replace(name, '.', '/') + '.py'
      if os.path.exists(path):
        importlib.import_module(name)

  def register(self, module):
    self.modules[slugify(module.name)] = module

  def get(self, name):
    return self.modules[name]

  def get_list(self):
    return [ module for key, module in self.modules.items()]


module_manager = ModuleManager()


