from django.core.management.base import BaseCommand
from espacios_obligados.models import Entidad
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Entidades data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 1

        for _ in range(num_registros):
            entidad = Entidad.objects.create(
                razon_social=fake.company(),
                cuit=random.randint(10000000000, 99999999999),
                sector=random.choice(["publica", "privada"]),
                tipo=random.choice(["Administracion Publica", "Entidad Financiera", "Institución educativa", "Institucion Recreativa", "Institucion de Salud"])
            )
            entidad.save()

        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {num_registros} registros en la tabla Entidad"))
