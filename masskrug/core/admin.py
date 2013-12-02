from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Group, Profile, GroupCategory

class GroupAdmin(MPTTModelAdmin):
  list_display = ('name', )
  prepopulated_fields = {
    'slug': ('name', ),
  }

class GroupCategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {
    'slug': ('name', ),
  }

class ProfileAdmin(admin.ModelAdmin):
  pass

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupCategory, GroupCategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
