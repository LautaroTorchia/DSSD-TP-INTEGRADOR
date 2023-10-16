# reservas/models.py

from django.db import models
from proveedores.models import ActorMaterial  # Importa el modelo ActorMaterial de tu aplicación existente

class ReservaMaterial(models.Model):
    material = models.ForeignKey(ActorMaterial, on_delete=models.CASCADE)
    fecha_entrega_pactada = models.DateField()

    def __str__(self):
        return f"Reserva de {self.material.material.nombre} para {self.material.actor.nombre} a entregar en {self.fecha_entrega_pactada}"

class ReservaLugarFabricacion(models.Model):
    ubicacion = models.CharField(max_length=100)
    fecha_inicio_reserva = models.DateField()
    fecha_fin_reserva = models.DateField()

    def __str__(self):
        return f"Reserva de lugar de fabricación en {self.ubicacion}"
