from django.core.management.base import BaseCommand
from espacios_obligados.models import Sede, Responsable
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Responsables data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 100

        for _ in range(num_registros):
            # Generar datos falsos
            nombre = fake.first_name()
            apellido = fake.last_name()
            telefono = fake.phone_number()
            email = fake.email()

            # Seleccionar una sede aleatoria para asociar al responsable
            sede = Sede.objects.order_by('?').first()

            # Crear el responsable y asociarlo a la sede
            responsable = Responsable.objects.create(
                sede_asignada=sede,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email
            )

            sede.responsables.add(responsable)

            self.stdout.write(self.style.SUCCESS(f'Se generó y guardó el Responsable: {responsable}'))
