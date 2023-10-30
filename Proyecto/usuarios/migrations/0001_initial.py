# Generated by Django 4.2.5 on 2023-10-29 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='Mail')),
                ('dni', models.PositiveIntegerField(default='', unique=True, verbose_name='DNI')),
                ('nombre', models.CharField(default='', max_length=20, verbose_name='Nombre')),
                ('apellido', models.CharField(default='', max_length=20, verbose_name='Apellido')),
                ('telefono', models.BigIntegerField(default='', verbose_name='Telefono')),
                ('is_active', models.BooleanField(default=True)),
                ('tipo_usuario', models.CharField(max_length=20, verbose_name='Tipo de Usuario')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'usuario',
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Provincias',
            fields=[
                ('provincia_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(default='', max_length=30, verbose_name='Nombre')),
                ('validez_certificado', models.PositiveIntegerField(default='', verbose_name='Validez del Certificado')),
            ],
            options={
                'verbose_name': 'provincia',
                'db_table': 'provincias',
            },
        ),
        migrations.CreateModel(
            name='Representante',
            fields=[
                ('representante_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'representante',
                'db_table': 'representantes',
            },
        ),
        migrations.CreateModel(
            name='AdminProvincial',
            fields=[
                ('admin_provincial_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('provincias', models.ManyToManyField(related_name='administradores_provinciales', to='usuarios.provincias')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'administrador provincial',
                'db_table': 'administradores_provinciales',
            },
        ),
    ]
