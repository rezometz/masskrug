from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import Group, Role, Profile, Module
from .forms import ConfirmForm
from .modules import module_manager

class ListGroupView(generic.ListView):
  model = Group

class ProfileListGroupView(ListGroupView):
  template_name = 'core/group_list_profile.html'

  def get_queryset(self, *args, **kwargs):
    queryset = super(ProfileListGroupView, self).get_queryset(*args, **kwargs)

    queryset = queryset.filter(users=self.request.user)
    queryset = queryset.order_by('category')

    return queryset


class GroupQueryJoinView(generic.FormView):
  form_class = ConfirmForm
  template_name = 'core/role_form_query_confirm.html'

  def post(self, request, *args, **kwargs):
    Role.objects.create(
      group=self.group,
      profile=request.user.profile,
    )

    messages.success(request,
      _("A request has been sent to the manager of the group.")
    )

    return super(GroupQueryJoinView, self).post(request, *args, **kwargs)

  def get_success_url(self, *args, **kwargs):
    return self.request.META['HTTP_REFERER']

  def dispatch(self, *args, **kwargs):
    self.group = Group.objects.get(slug=self.kwargs['slug'])

    return super(GroupQueryJoinView, self).dispatch(*args, **kwargs)

  def get_context_data(self, *args, **kwargs):
    context = super(GroupQueryJoinView, self).get_context_data(*args, **kwargs)
    context['group'] = self.group

    return context

class GroupHomeView(generic.DetailView):
  model = Group

  def get_context_data(self, *args, **kwargs):
    context = super(GroupHomeView, self).get_context_data(*args, **kwargs)

    self.group = self.get_object()

    context['modules'] = []
    javascript = []
    stylesheets = []
    
    for key, module in module_manager.modules.items():
      for view_name, view in module.views.items():
        context['modules'].append({
          'template': view.template_name,
        })
        context.update(
          view.get_context_data(self.request, content_object=self.group)
        )
        stylesheets += view.Meta.stylesheets
        javascript += view.Meta.javascript

    context['stylesheets'] = stylesheets
    context['javascript'] = javascript
  
    return context

class GroupMemberListView(generic.ListView):
  model = Role
  template_name = 'core/group_member_list.html'
  context_object_name = 'member_roles'

  def get_queryset(self, *args, **kwargs):
    queryset = super(GroupMemberListView, self).get_queryset(*args, **kwargs)

    queryset = queryset.filter(group=self.group)

    return queryset

  def dispatch(self, *args, **kwargs):
    self.group = Group.objects.get(slug=self.kwargs['slug'])

    return super(GroupMemberListView, self).dispatch(*args, **kwargs)

  def get_context_data(self, *args, **kwargs):
    context = super(GroupMemberListView, self).get_context_data(*args, **kwargs)
    context['group'] = self.group

    return context

class GroupModuleListView(generic.ListView):
  model = Module
  template_name = 'core/group_module_list.html'
  context_object_name = 'modules'

  def get_queryset(self, *args, **kwargs):
    queryset = super(GroupModuleListView, self).get_queryset(*args, **kwargs)

    queryset = queryset.filter(group=self.group)

    return queryset

  def dispatch(self, *args, **kwargs):
    self.group = Group.objects.get(slug=self.kwargs['slug'])

    return super(GroupModuleListView, self).dispatch(*args, **kwargs)

  def get_context_data(self, *args, **kwargs):
    context = super(GroupModuleListView, self).get_context_data(*args, **kwargs)
    context['group'] = self.group
    context['modules_disabled'] = module_manager.get_list()

    return context

class GroupModuleEnabledToggleView(generic.FormView):
  form_class= ConfirmForm
  template_name = 'core/group_module_enabled_toggle.html'

  def post(self, request, *args, **kwargs):

    self.module.enabled = True if self.created else not self.module.enabled
    self.module.save()

    messages.success(request,
      _("The <b>%(module_name)s</b> settings has been modified.") % {
        'module_name': self.kwargs['module'],
      }
    )

    return super(GroupModuleEnabledToggleView, self).post(request, *args, **kwargs)

  def dispatch(self, *args, **kwargs):
    self.group = Group.objects.get(slug=self.kwargs['slug'])

    (self.module, self.created) = Module.objects.get_or_create(
      group=self.group,
      name=self.kwargs['module'],
    )
    return super(GroupModuleEnabledToggleView, self).dispatch(*args, **kwargs)

  def get_context_data(self, *args, **kwargs):
    context = super(GroupModuleEnabledToggleView, self).get_context_data(*args, **kwargs)
    context['group'] = self.group
    context['module'] = self.module

    return context

  def get_success_url(self, *args, **kwargs):
    return reverse('group-home', kwargs={
      'slug': self.group.slug,
    })
