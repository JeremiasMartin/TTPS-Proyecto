from django.db import models
from usuarios.models import Representante, Provincias, Certificante
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
    responsables = models.ManyToManyField('Responsable', blank=True, related_name='responsables')
    
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
        return '%s , %s' % (self.nombre, self.provincia) 
    

class EspacioObligado(models.Model):
    estado = models.CharField(max_length=100,default='EN PROCESO')  # Agregando el campo estado
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    motivo = models.TextField(blank=True,default='')
    fecha_creacion = models.DateField()
    def __str__(self):
        return f'!nombre sede {self.sede.nombre} y estado{self.estado}'

class DEA(models.Model):
    dea_sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    numero_serie = models.CharField(max_length=200)
    nombre_representativo = models.CharField(max_length=200)
    solidario = models.BooleanField(default=False)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')

    def __str__(self):
        return self.nombre_representativo
    

class HistorialDEA(models.Model):
    dea = models.ForeignKey(DEA, on_delete=models.CASCADE)
    dia = models.DateField()
    servicio = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.dea.nombre_representativo


class Responsable(models.Model):
    sede_asignada = models.ForeignKey(Sede, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre + " " + self.apellido
    

class SolicitudAprobacion(models.Model):
    representante = models.ForeignKey(Representante, on_delete=models.CASCADE)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    motivo = models.TextField()
    aprobado = models.BooleanField(default=False)
    estado = models.TextField(default='', blank=True)
    def __str__(self):
        return f'nombre sede {self.sede.nombre} y estado{self.estado}'


class Visita(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    observaciones = models.TextField()
    resultado = models.CharField(max_length=20, choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')])
    espacio_obligado_id = models.ForeignKey(EspacioObligado, on_delete=models.CASCADE)
    certificante_id = models.ForeignKey(Certificante, on_delete=models.CASCADE, null=True, blank=True)

class EventoMuerteSubita(models.Model):
    fecha = models.DateField()
    sexo = models.CharField(max_length=20, choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')])
    edad = models.IntegerField()
    fallecido = models.BooleanField(default=False)
    rcp = models.BooleanField(default=False)
    tiempo_rcp = models.IntegerField(null=True, blank=True)
    dea = models.ForeignKey(DEA, on_delete=models.CASCADE, null=True, blank=True)
    inconveniente = models.CharField(max_length=250, blank=True, null=True)
    descarga_electrica = models.BooleanField(default=False, null=True, blank=True)
    cantidad_descarga = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    sede_id = models.ForeignKey(Sede, on_delete=models.CASCADE)
    representante_id = models.ForeignKey(Representante, on_delete=models.CASCADE)