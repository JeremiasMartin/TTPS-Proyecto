from django.db import models
from django.contrib.gis.db import models as gis_models

class EntidadDW(models.Model):
    razon_social = models.CharField(max_length=200)
    cuit = models.CharField(max_length=200)
    sector = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)

    class Meta:
        app_label = 'datawarehouse'

    def __str__(self):
        return self.razon_social

class SedeDW(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = gis_models.PointField()
    direccion = models.CharField(max_length=200)
    entidad = models.ForeignKey(EntidadDW, on_delete=models.CASCADE)
    representantes = models.ManyToManyField('RepresentanteDW', blank=True, related_name='representantes')

    class Meta:
        app_label = 'datawarehouse'

    def __str__(self):
        return '%s , %s' % (self.nombre, self.entidad)

class EspacioObligadoDW(models.Model):
    estado = models.CharField(max_length=100, default='EN PROCESO')
    sede = models.ForeignKey(SedeDW, on_delete=models.CASCADE)
    motivo = models.TextField(blank=True, default='')
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'datawarehouse'

    def __str__(self):
        return f'!nombre sede {self.sede.nombre} y estado{self.estado}'

class DEADW(models.Model):
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    solidario = models.BooleanField(default=False)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')

    class Meta:
        app_label = 'datawarehouse'

    def __str__(self):
        return self.nombre_representativo

class EventoMuerteSubitaDW(models.Model):
    fecha = models.DateField()
    observaciones = models.TextField()
    resultado = models.CharField(max_length=20, choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')])
    sede_id = models.ForeignKey(SedeDW, on_delete=models.CASCADE)

    class Meta:
        app_label = 'datawarehouse'

    def __str__(self):
        return f'Evento en {self.sede.nombre} el {self.fecha}'
    
class RepresentanteDW(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    dni = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    sede_id = models.ForeignKey(SedeDW, on_delete=models.CASCADE)

    class Meta:
        app_label = 'datawarehouse'
        
    def __str__(self):
        return self.nombre

# Otros modelos como RepresentanteDW, ProvinciasDW, CertificanteDW pueden ser agregados según sea necesario.

