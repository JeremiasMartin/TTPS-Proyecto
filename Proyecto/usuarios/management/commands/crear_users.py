from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Usuarios data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 10
        representantes_count=num_registros//2
        i=0
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
            usuario.save()
            i += 1

        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {num_registros} registros en la tabla Usuario"))