from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField
from mptt.models import MPTTModel, TreeForeignKey

from .modules import module_manager

class GroupCategory(models.Model):
  name = models.CharField(
    _('Name'),
    max_length=50,
    unique=True,
  )

  slug = models.SlugField(
    _('Slug'),
  )

  description = models.TextField(
    _('Description'),
  )

  def __unicode__(self):
    return self.name

class Group(MPTTModel):
  name = models.CharField(
    _('Name'),
    max_length=30,
    unique=True,
  )

  category = models.ForeignKey(
    GroupCategory,
    related_name='groups',
    null=True,
    blank=True,
  )

  slug = models.SlugField(
    _('Slug'),
  )

  hidden = models.BooleanField(
    _('Hidden'),
    default=False,
  )

  parent = TreeForeignKey(
    'self',
    null=True,
    blank=True,
    related_name='children',
  )

  description = models.TextField(
    _('Description'),
  )

  color = RGBColorField(_('Color'))

  icon = models.ImageField(
    _('Image'),
    upload_to='core/group/icon',
    blank=True,
    null=True,
  )

  def __unicode__(self):
    return self.name

  class MPTTMeta:
    order_insertion_by = ['name']

class Profile(models.Model):
  user = models.OneToOneField(
    User,
    related_name='profile',
  )

  groups = models.ManyToManyField(
    Group,
    related_name='users',
    through='Role',
  )

class GenericRole(models.Model):
  title = models.CharField(
    _('Title'),
    max_length=40,
  )

  def __unicode__(self):
    return self.title

class Role(models.Model):
  title = models.CharField(
    _('Title'),
    max_length=40,
    blank=True
  )
  
  group = models.ForeignKey(
    Group,
  )
  
  profile = models.ForeignKey(
    Profile,
  )
  
  generic_role = models.ForeignKey(
    GenericRole,
    default=None,
    null=True,
    blank=True,
  )

  enabled = models.BooleanField(
    _('Enabled'),
    default=True,
  )

  accepted = models.BooleanField(
    _('Valid'),
    default=False,
  )
  
  def __unicode__(self):
    return self.title

class Module(models.Model):
  group = models.ForeignKey(
    Group,
    related_name='modules',
  )

  name = models.CharField(
    _('Name'),
    max_length=50,
  )

  enabled = models.BooleanField(
    _('Enabled'),
    default=False,
  )

  def get_module(self):
    return module_manager.get(self.name)

  def __unicode__(self):
    return self.name
