from django.db import models


class DimFechaLog(models.Model):
    idFechaLog = models.AutoField(primary_key=True)
    dia = models.IntegerField()
    mes = models.IntegerField()
    anho = models.IntegerField()

class DimFechaCreacion(models.Model):
    idFechaCreacion = models.AutoField(primary_key=True)
    dia = models.IntegerField()
    mes = models.IntegerField()
    anho = models.IntegerField()

class DimFechaEventoMS(models.Model):
    idFechaEvento = models.AutoField(primary_key=True)
    dia = models.IntegerField()
    mes = models.IntegerField()
    anho = models.IntegerField()

class DimEstado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    nombreEstado = models.CharField(max_length=100)
    fecha_creacion = models.ForeignKey(DimFechaLog, on_delete=models.CASCADE)
    idSede = models.ForeignKey('DimSede', on_delete=models.CASCADE)
    

class DimSede(models.Model):
    idTipoSede = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    fecha_creacion = models.ForeignKey(DimFechaCreacion, on_delete=models.CASCADE)
    idLugar = models.ForeignKey('DimLugar', on_delete=models.CASCADE)
    idEstado = models.ForeignKey(DimEstado, null=True, blank=True, on_delete=models.CASCADE)

class DimLugar(models.Model):
    idLugar = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)


# Representante con que tabla debe asociarse?
# class DimRepresentante(models.Model):
#     idRepresentante = models.AutoField(primary_key=True)
#     fecha_nacimiento = models.DateField()

class DimDEA(models.Model):
    idDEA = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    idSede = models.ForeignKey(DimSede, on_delete=models.CASCADE)

class DimMuerteSubita(models.Model):
    idMuerteSubita = models.AutoField(primary_key=True)
    sexo = models.CharField(max_length=1, choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")])
    edad = models.IntegerField()
    idSede = models.ForeignKey(DimSede, on_delete=models.CASCADE)
    idFecha = models.ForeignKey(DimFechaEventoMS, on_delete=models.CASCADE)
    inSitu = models.BooleanField(default=False)
    dea = models.ForeignKey(DimDEA, null=True, blank=True, on_delete=models.CASCADE)
    


class Hechos(models.Model):
    idHecho = models.AutoField(primary_key=True)
    idEstado = models.ForeignKey(DimEstado, on_delete=models.CASCADE)
    idSede = models.ForeignKey(DimSede, on_delete=models.CASCADE)
    idLugar = models.ForeignKey(DimLugar, on_delete=models.CASCADE)
    cantEspaciosObligados = models.IntegerField()
    cantDeas = models.IntegerField()
    cantDEAsSolidarios = models.IntegerField()
    cantMuertesSubitas = models.IntegerField()
    cantMuertesInSitu = models.IntegerField()
