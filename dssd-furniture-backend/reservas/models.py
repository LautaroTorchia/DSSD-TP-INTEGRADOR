# reservas/models.py

from django.db import models

class LugarDeFabricacion(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    internacional = models.BooleanField(default=True)
    
    
class ReservaMaterial(models.Model):
    id_venta_proveedor= models.IntegerField()
    nombre_proveedor = models.CharField(max_length=100)
    nombre_material = models.CharField(max_length=100)
    cantidad_pactada= models.IntegerField()
    fecha_entrega_pactada = models.DateField()
    sede_a_entregar = models.ForeignKey(LugarDeFabricacion,on_delete=models.CASCADE)

class ReservaLugarFabricacion(models.Model):
    lugar_de_fabricacion= models.ForeignKey(LugarDeFabricacion,on_delete=models.CASCADE)
    fecha_inicio_reserva = models.DateField()
    fecha_fin_reserva = models.DateField()

    def __str__(self):
        return f"Reserva de lugar de fabricación en {self.lugar_de_fabricacion.ubicacion}"


class MaterialEntregado(models.Model):
    id_reserva= models.ForeignKey(ReservaMaterial,on_delete=models.CASCADE)
    dia_entregad=models.DateField()
    