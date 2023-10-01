from django.contrib import admin
from .models import BonitaAPICall

@admin.register(BonitaAPICall)
class BonitaAPICallAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'endpoint_called', 'request_data')
    list_filter = ('timestamp', 'endpoint_called')
    search_fields = ('endpoint_called', 'request_data')