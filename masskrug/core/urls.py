from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import Group
from .views import ProfileListGroupView, \
  GroupQueryJoinView, GroupHomeView, GroupMemberListView, \
  GroupModuleListView, GroupModuleEnabledToggleView
from .modules import module_manager

module_manager.autodiscover()

urlpatterns = patterns('',

  # Group list
  url(r'^groups$',
    generic.ListView.as_view(model=Group),
    name="group-list",
  ),
  
  # Profile group list
  url(r'^profile/groups$',
    login_required(ProfileListGroupView.as_view()),
    name="profile-groups",
  ),

  # Query for joining group
  url(r'^group/(?P<slug>[\w-]+)/join$',
    login_required(GroupQueryJoinView.as_view()),
    name="group-join",
  ),

  # Group Home
  url(r'^group/(?P<slug>[\w-]+)/home$',
    GroupHomeView.as_view(),
    name="group-home",
  ),

  # Group Member List (members)
  url(r'^group/(?P<slug>[\w-]+)/members/list$',
    GroupMemberListView.as_view(),
    name="group-member-list",
  ),

  # Group Module List
  url(r'^group/(?P<slug>[\w-]+)/modules$',
    GroupModuleListView.as_view(),
    name="group-module-list",
  ),

  # Enable Module
  url(r'^group/(?P<slug>[\w-]+)/module/(?P<module>[\w-]+)$',
    GroupModuleEnabledToggleView.as_view(),
    name="group-module-enabled-toggle",
  ),
)
