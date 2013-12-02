from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField
from mptt.models import MPTTModel, TreeForeignKey

class Group(MPTTModel):
  name = models.CharField(
    _('Name'),
    max_length=30,
    unique=True,
  )

  slug = models.SlugField(
    _('Slug'),
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
  )
