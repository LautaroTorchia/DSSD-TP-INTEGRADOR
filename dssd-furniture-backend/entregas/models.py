from django.db import models
from furniture_collection.models import Coleccion

# Create your models here.
class VendedorFinal(models.Model):
    nombre=models.CharField(max_length=100)
    ubicacion=models.CharField(max_length=100)
    telefono=models.CharField(max_length=100)
    
class OrdenDeEntrega(models.Model):
    descripcion=models.CharField(max_length=100)
    fecha_entrega=models.DateField()
    id_coleccion=models.ForeignKey(Coleccion,on_delete=models.CASCADE)
    vendedor_final=models.ForeignKey(VendedorFinal, on_delete=models.CASCADE)
    se_entrego=models.BooleanField()

class LotesFabricados(models.Model):
    fecha_fabricado=models.DateField()
    coleccion=models.ForeignKey(Coleccion,on_delete=models.CASCADE)
    lugar=models.IntegerField()
    
class SedeDeDistribucion(models.Model):
    nombre=models.CharField(max_length=100)
    ubicacion=models.CharField(max_length=100)

class AsociacionLoteOrdenEntrega(models.Model):
    orden_entrega=models.ForeignKey(OrdenDeEntrega,on_delete=models.CASCADE)
    lote=models.ForeignKey(LotesFabricados,on_delete=models.CASCADE)
    fecha_asociacion=models.DateField(auto_now_add=True)

class AsociacionLoteDistribucion(models.Model):
    distribucion=models.ForeignKey(SedeDeDistribucion,on_delete=models.CASCADE)
    lote=models.ForeignKey(LotesFabricados,on_delete=models.CASCADE)
    fecha_asociacion=models.DateField(auto_now_add=True)
