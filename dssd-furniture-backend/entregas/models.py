from django.db import models
from furniture_collection.models import Coleccion

# Create your models here.

class OrdenDeEntrega(models.Model):
    descripcion=models.CharField(max_length=100)
    fecha_entrega=models.DateField()
    id_coleccion=models.ForeignKey(Coleccion,on_delete=models.CASCADE)
    se_entrego=models.BooleanField()
    