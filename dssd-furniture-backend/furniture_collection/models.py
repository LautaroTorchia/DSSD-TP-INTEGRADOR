from django.db import models


class Coleccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    diseñada = models.BooleanField(default=False)
    fabricada = models.BooleanField(default=False)
    instancia_bonita = models.IntegerField(null=True)
    fecha_lanzamiento_estimada = models.DateField()

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Colecciones"  # Aquí especificamos el nombre plural deseado
    
    

class Mueble(models.Model):
    nombre = models.CharField(max_length=100)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    plazo_fabricacion = models.PositiveIntegerField()  # En días
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100)
    plan_fabricacion = models.CharField(max_length=100) 
    materiales = models.CharField(max_length=255)  # Change to CharField
    
    class Meta:
        unique_together = ('nombre', 'coleccion')
        verbose_name_plural = "Muebles" 

    def __str__(self):
        return self.nombre