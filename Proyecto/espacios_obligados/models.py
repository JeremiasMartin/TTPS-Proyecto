from django.db import models
from usuarios.models import Representante, Provincias
from django.contrib.gis.db import models as gis_models

# Create your models here.

class Entidad(models.Model):
    id = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=200)
    cuit = models.CharField(max_length=200)
    sector = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    def __str__(self):
        return self.razon_social
    

class Sede(models.Model):
    representantes = models.ManyToManyField(Representante)
    nombre = models.CharField(max_length=200)
    cant_personas_externas = models.IntegerField(default=0)
    superficie = models.IntegerField(default=0)
    ubicacion = gis_models.PointField()
    cant_personal = models.IntegerField(default=0)
    direccion = models.CharField(max_length=200)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

    def __str__(self):
        return '%s , %s' % (self.nombre, self.provincia) 
    

class EspacioObligado(models.Model):
    estado = models.CharField(max_length=100,default='EN PROCESO')  # Agregando el campo estado
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    motivo= models.TextField(blank=True,default='')
    def __str__(self):
        return self.estado