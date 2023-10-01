from import_export import resources
from .models import Role, HeadRole, UserRole, ViewDescriptor, PermissionRole, EventSuspensionRole

class RoleResource(resources.ModelResource):
    class Meta:
        model = Role

class HeadRoleResource(resources.ModelResource):
    class Meta:
        model = HeadRole

class UserRoleResource(resources.ModelResource):
    class Meta:
        model = UserRole

class ViewDescriptorResource(resources.ModelResource):
    class Meta:
        model = ViewDescriptor

class PermissionRoleResource(resources.ModelResource):
    class Meta:
        model = PermissionRole

class EventSuspensionRoleResource(resources.ModelResource):
    class Meta:
        model = EventSuspensionRole        