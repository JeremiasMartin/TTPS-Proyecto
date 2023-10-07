# Generated by Django 4.2.5 on 2023-10-06 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
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
