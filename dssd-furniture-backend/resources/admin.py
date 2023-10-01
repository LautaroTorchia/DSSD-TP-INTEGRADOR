from django.contrib import admin
from .models import Resource, ConfigMessage, ConfigResource, UserTranslation
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.resources import ModelResource


class ResourceImplResource(ModelResource):

    class Meta:
        model = Resource

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class ResourceAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'keywords', 'created_at']
    resource_class = ResourceImplResource        

class ConfigMessageResource(ModelResource):

    class Meta:
        model = ConfigMessage

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class ConfigMessageAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'keywords', 'created_at']
    resource_class = ConfigMessageResource         

class ConfigResourceImplResource(ModelResource):

    class Meta:
        model = ConfigResource

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class ConfigResourceAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'keywords', 'created_at']
    resource_class = ConfigResourceImplResource

class UserTranslationResource(ModelResource):

    class Meta:
        model = UserTranslation

    def for_delete(self, row, instance):
        return self.fields['created_at'].clean(row) == ''

class UserTranslationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id_message_config', 'language', 'created_at']
    resource_class = UserTranslationResource

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ConfigMessage, ConfigMessageAdmin)
admin.site.register(ConfigResource, ConfigResourceAdmin)
admin.site.register(UserTranslation, UserTranslationAdmin)