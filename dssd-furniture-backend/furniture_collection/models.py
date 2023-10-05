from django.db import models
from django.utils import timezone

class Coleccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    terminada = models.BooleanField(default=False)
    instancia_bonita = models.IntegerField()

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Colecciones"  # Aquí especificamos el nombre plural deseado
    
    

class Mueble(models.Model):
    nombre = models.CharField(max_length=100)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    plazo_fabricacion = models.PositiveIntegerField()  # En días
    fecha_lanzamiento_estimada = models.DateField()
    descripcion = models.TextField()
    imagen = models.URLField(blank=True)  # URL de la imagen en el repositorio documental
    plan_fabricacion = models.URLField(blank=True)  # URL del plan de fabricación en el repositorio documental
    materiales = models.TextField()
    
    class Meta:
        unique_together = ('nombre', 'coleccion')
        verbose_name_plural = "Muebles" 

    def __str__(self):
        return self.nombre