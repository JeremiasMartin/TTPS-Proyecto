from django.core.management.base import BaseCommand
from usuarios.models import AdminProvincial, Certificante, Provincias, Representante, Usuario
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Usuarios data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 10
        representantes_count=num_registros//2
        provincias_existentes = Provincias.objects.all()
        i=0
        self.stdout.write(self.style.SUCCESS(f"Inicio creación de usuarios...."))
        for _ in range(num_registros):
            usuario = Usuario.objects.create(
                email=fake.email(),
                password= "pbkdf2_sha256$600000$RqEMWbt4iQ9bunchq4pVPB$HbpJHULaZA9iRq/hDjzrD4QvyEotG779O2UkmPwR9hs=", #0oeeuke0
                dni=random.randint(10000000, 99999999),
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                telefono=random.randint(1000000000, 9999999999),               
            ) 
            if i < representantes_count:
                usuario.tipo_usuario="representante"
            else:
                usuario.tipo_usuario=random.choice(["admin_provincial", "certificante"])  # Ajusta los tipos según tus necesidades

            cantidad_provincias = random.randint(1, 3)
            if usuario.tipo_usuario == 'representante':
                Representante.objects.create(user=usuario)
            elif usuario.tipo_usuario == 'admin_provincial':
                admin_provincial = AdminProvincial.objects.create(user=usuario)
                provincias_seleccionadas = random.sample(list(provincias_existentes), cantidad_provincias)
                admin_provincial.provincias.set(provincias_seleccionadas)
            elif usuario.tipo_usuario == 'certificante':
                certificante = Certificante.objects.create(user=usuario)
                provincias_seleccionadas = random.sample(list(provincias_existentes), cantidad_provincias)
                certificante.provincias.set(provincias_seleccionadas)

            usuario.save()
            i += 1
        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {num_registros} registros en la tabla Usuario"))