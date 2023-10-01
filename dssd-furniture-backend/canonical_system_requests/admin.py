from django.contrib import admin
from .models import SystemRequest
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.resources import ModelResource


class SystemRequestResource(ModelResource):

    class Meta:
        model = SystemRequest

    def for_delete(self, row, instance):
        return self.fields['denomination_command'].clean(row) == ''

class SystemRequestAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['denomination_command', 'created_at']
    resource_class = SystemRequestResource

admin.site.register(SystemRequest, SystemRequestAdmin)
