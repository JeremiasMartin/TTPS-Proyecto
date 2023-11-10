from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models as gis_models


class UsuarioManager(BaseUserManager):

    def create_user(self, email, nombre, apellido, dni, telefono, password=None):
        if not email:
            raise ValueError(
                'El usuario debe especificar un correo electrónico.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.dni = dni
        user.nombre = nombre
        user.apellido = apellido
        user.telefono = telefono
        user.save()
        return user

    def create_superuser(self, email, password, nombre, apellido, dni, telefono):
        user = self.create_user(email=email, nombre=nombre, apellido=apellido,
                                dni=dni, telefono=telefono, password=password)
        user.is_admin = True
        user.is_staff = True
        user.tipo_usuario = 'admin'
        user.save()
        return user


class Usuario(AbstractBaseUser):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(
        'Mail', unique=True, max_length=254, blank=True, null=False)
    dni = models.PositiveIntegerField(
        'DNI', unique=True, blank=False, null=False, default='')
    nombre = models.CharField('Nombre', max_length=20,
                              blank=False, null=False, default='')
    apellido = models.CharField(
        'Apellido', max_length=20, blank=False, null=False, default='')
    telefono = models.BigIntegerField(
        'Telefono', blank=False, null=False, default='')
    is_active = models.BooleanField(default=True)
    tipo_usuario = models.CharField(
        'Tipo de Usuario', max_length=20, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UsuarioManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'usuario'
        db_table = 'usuarios'

    def __str__(self):
        return '%s, %s' % (self.email, self.tipo_usuario)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Representante(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    representante_id = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'representante'
        db_table = 'representantes'

    def __str__(self) -> str:
        return '%s, %s' % (self.user.apellido, self.user.nombre)

    def save(self, *args, **kwargs):
        self.user.tipo_usuario = 'representante'
        self.user.save()
        super().save(*args, **kwargs)


class Provincias(models.Model):
    provincia_id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=30,
                              blank=False, null=False, default='')
    validez_certificado = models.PositiveIntegerField(
        'Validez del Certificado', blank=False, null=False, default='')

    class Meta:
        verbose_name = 'provincia'
        db_table = 'provincias'

    def __str__(self) -> str:
        return '%s' % (self.nombre)


class AdminProvincial(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    admin_provincial_id = models.AutoField(primary_key=True)
    provincias = models.ManyToManyField(
        Provincias, related_name='administradores_provinciales')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'administrador provincial'
        db_table = 'administradores_provinciales'

    def __str__(self) -> str:
        return '%s, %s' % (self.user.apellido, self.user.nombre)

    def save(self, *args, **kwargs):
        self.user.tipo_usuario = 'admin_provincial'
        self.user.save()
        super().save(*args, **kwargs)



class UsuarioComun(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    usuario_comun_id = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'usuario_comun'
        db_table = 'usuarios_comunes'
          
    def __str__(self) -> str:
        return '%s, %s' % (self.user.apellido, self.user.nombre)
      
    def save(self, *args, **kwargs):
        self.user.tipo_usuario = 'comun'
        self.user.save()
        super().save(*args, **kwargs)

        
class Certificante(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    certificante_id = models.AutoField(primary_key=True)
    provincias = models.ManyToManyField(
        Provincias, related_name='certificantes_provinciales')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'certificante'
        db_table = 'certificantes'


    def __str__(self) -> str:
        return '%s, %s' % (self.user.apellido, self.user.nombre)

    def save(self, *args, **kwargs):
        self.user.tipo_usuario = 'comun'
        self.user.save()
        super().save(*args, **kwargs)
    
        self.user.tipo_usuario = 'certificante'
        self.user.save()
        super().save(*args, **kwargs)

    def agregar_provincias(self, provincias_ids):
        for provincia_id in provincias_ids:
            provincia = Provincias.objects.get(pk=provincia_id)
            self.provincias.add(provincia)

    def quitar_provincias(self, provincias_ids):
        for provincia_id in provincias_ids:
            provincia = Provincias.objects.get(pk=provincia_id)
            self.provincias.remove(provincia)
