# reservas/models.py

from django.db import models
from proveedores.models import ActorMaterial
from proveedores.models import LugarDeFabricacion
   
class ReservaMaterial(models.Model):
    id_venta_proveedor= models.ForeignKey(ActorMaterial,on_delete=models.CASCADE)
    cantidad_pactada= models.IntegerField()
    fecha_entrega_pactada = models.DateField()
    sede_a_entregar = models.ForeignKey(LugarDeFabricacion,on_delete=models.CASCADE)

class ReservaLugarFabricacion(models.Model):
    lugar_de_fabricacion= models.IntegerField()
    fecha_inicio_reserva = models.DateField()
    fecha_fin_reserva = models.DateField()

    def __str__(self):
        return f"Reserva de lugar de fabricación en {self.lugar_de_fabricacion.ubicacion}"
