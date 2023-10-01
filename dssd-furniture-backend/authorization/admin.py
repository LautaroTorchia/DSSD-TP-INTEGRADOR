from django.contrib import admin
from .models import Role, HeadRole, UserRole, ViewDescriptor, PermissionRole, EventSuspensionRole
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.resources import ModelResource


class RoleResource(ModelResource):

    class Meta:
        model = Role

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class RoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['denomination', 'is_archived']
    resource_class = RoleResource

class HeadRoleResource(ModelResource):

    class Meta:
        model = HeadRole

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class HeadRoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['child', 'head', 'observations']
    resource_class = HeadRoleResource


class UserRoleResource(ModelResource):

    class Meta:
        model = UserRole

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class UserRoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['user_id', 'role_id']
    resource_class = UserRoleResource


class ViewDescriptorResource(ModelResource):

    class Meta:
        model = ViewDescriptor

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class ViewDescriptorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['denomination', 'stack_name']
    resource_class = ViewDescriptorResource

class PermissionRoleResource(ModelResource):

    class Meta:
        model = PermissionRole

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class PermissionRoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['view_id', 'role_id']
    resource_class = PermissionRoleResource

class EventSuspensionRoleResource(ModelResource):

    class Meta:
        model = EventSuspensionRole

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class EventSuspensionRoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['role_id', 'start_at', 'end_at']
    resource_class = EventSuspensionRoleResource


admin.site.register(Role, RoleAdmin)
admin.site.register(HeadRole, HeadRoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(ViewDescriptor, ViewDescriptorAdmin)
admin.site.register(PermissionRole, PermissionRoleAdmin)
admin.site.register(EventSuspensionRole, EventSuspensionRoleAdmin)