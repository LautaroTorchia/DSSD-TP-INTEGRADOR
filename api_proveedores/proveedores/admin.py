from django.contrib import admin
from .models import Actor, Material, ActorMaterial

# Register the Actor model
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_actor', 'ubicacion')

# Register the Material model
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

# Register the ActorMaterial model
@admin.register(ActorMaterial)
class ActorMaterialAdmin(admin.ModelAdmin):
    list_display = ('actor', 'material', 'cantidad_disponible', 'plazo_entrega_dias')
