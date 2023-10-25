# reservas/models.py

from django.db import models
from proveedores.models import ActorMaterial  # Importa el modelo ActorMaterial de tu aplicación existente

class ReservaMaterial(models.Model):
    id_venta_proveedor= models.IntegerField()
    nombre_proveedor = models.CharField(max_length=100)
    nombre_material = models.CharField(max_length=100)
    cantidad_pactada= models.IntegerField()
    fecha_entrega_pactada = models.DateField()

class LugarDeFabricacion(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    internacional = models.BooleanField(default=True)
    
class ReservaLugarFabricacion(models.Model):
    lugar_de_fabricacion= models.ForeignKey(LugarDeFabricacion,on_delete=models.CASCADE)
    fecha_inicio_reserva = models.DateField()
    fecha_fin_reserva = models.DateField()

    def __str__(self):
        return f"Reserva de lugar de fabricación en {self.lugar_de_fabricacion.ubicacion}"

    