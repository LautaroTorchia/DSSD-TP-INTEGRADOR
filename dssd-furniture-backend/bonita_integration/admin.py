from django.contrib import admin
from .models import BonitaAPICall,BonitaCookies

@admin.register(BonitaAPICall)
class BonitaAPICallAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'endpoint_called', 'request_data')
    list_filter = ('timestamp', 'endpoint_called')
    search_fields = ('endpoint_called', 'request_data')

@admin.register(BonitaCookies)
class BonitaCookiesAdmin(admin.ModelAdmin):
    list_display = ('user', 'BOS_Locale', 'JSESSIONID','X_Bonita_API_Token')
    list_filter = ('user', 'BOS_Locale')
    search_fields = ('user', 'BOS_Locale')