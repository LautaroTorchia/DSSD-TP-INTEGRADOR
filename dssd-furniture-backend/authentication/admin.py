from django.contrib import admin
from .models import User
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.resources import ModelResource


class UserResource(ModelResource):

    class Meta:
        model = User

    def for_delete(self, row, instance):
        return self.fields['email'].clean(row) == ''


class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']
    resource_class = UserResource

admin.site.register(User, UserAdmin)