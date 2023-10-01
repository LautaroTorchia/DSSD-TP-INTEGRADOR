from django.contrib import admin
from .models import Coleccion, Mueble

class MuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'coleccion', 'plazo_fabricacion', 'fecha_lanzamiento_estimada')
    list_filter = ('coleccion',)
    search_fields = ('nombre', 'coleccion__nombre')

class ColeccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

admin.site.register(Coleccion, ColeccionAdmin)
admin.site.register(Mueble, MuebleAdmin)