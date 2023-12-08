from django.core.management.base import BaseCommand
from espacios_obligados.models import EspacioObligado
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Espacios Obligados data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 1

        for _ in range(num_registros):
            espacio_obligado = EspacioObligado.objects.create(
                estado=random.choice(["CARDIO ASISTIDO CERTIFICADO", "EN PROCESO", "CARDIO ASISTIDO", "CARDIO ASISTIDO CON CERTIFICADO VENCIDO"]),
                motivo=fake.text()
            )

        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {num_registros} registros en la tabla EspacioObligado"))
