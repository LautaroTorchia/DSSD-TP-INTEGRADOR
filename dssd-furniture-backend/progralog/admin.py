from django.contrib import admin
from .models import Progralog
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.resources import ModelResource


class ProgralogResource(ModelResource):

    class Meta:
        model = Progralog

    def for_delete(self, row, instance):
        return self.fields['event_type'].clean(row) == ''

class ProgralogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['event_type', 'created_at']
    resource_class = ProgralogResource

admin.site.register(Progralog, ProgralogAdmin)
