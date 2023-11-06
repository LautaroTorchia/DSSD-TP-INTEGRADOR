from django.db import models

class Actor(models.Model):
    TIPO_CHOICES = [
        ('Proveedor', 'Proveedor'),
        ('Productor', 'Productor'),
        ('Reciclador', 'Reciclador'),
    ]
    nombre = models.CharField(max_length=100)
    tipo_actor = models.CharField(max_length=10, choices=TIPO_CHOICES)
    ubicacion = models.CharField(max_length=100)
    internacional = models.BooleanField()
    
    class Meta:
        unique_together = ('nombre','tipo_actor')

    def __str__(self):
        return self.nombre

class Material(models.Model):
    nombre = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nombre

class ActorMaterial(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad_disponible = models.PositiveIntegerField()
    plazo_entrega_dias = models.PositiveIntegerField()
    es_importado= models.BooleanField()

    def __str__(self):
        return f"{self.actor.nombre} - {self.material.nombre}"
