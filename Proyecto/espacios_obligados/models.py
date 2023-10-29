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

    # Declaración Jurada
    
    personal_capacitado = models.BooleanField(default=False)
    senaletica = models.BooleanField(default=False)
    protocolo_accion = models.BooleanField(default=False)
    sistema_emergencia = models.BooleanField(default=False)
    deas_registrados = models.ManyToManyField('DEA', blank=True)
    deas_decreto = models.IntegerField(default=0)


    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    

class DEA(models.Model):
    dea_sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    aprobacion_ANMAT = models.BooleanField(default=False)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    numero_serie = models.CharField(max_length=200)
    nombre_representativo = models.CharField(max_length=200)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')

    def __str__(self):
        return self.sede.nombre
    

class HistorialDEA(models.Model):
    dea = models.ForeignKey(DEA, on_delete=models.CASCADE)
    dia = models.DateField()
    servicio = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.dea.nombre_representativo
