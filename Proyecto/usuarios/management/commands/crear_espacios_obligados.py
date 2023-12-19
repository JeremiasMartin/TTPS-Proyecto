from django.core.management.base import BaseCommand
from espacios_obligados.models import EspacioObligado, Sede
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Espacios Obligados data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 1000

        # Obtener todas las sedes existentes
        sedes_disponibles = list(Sede.objects.all())

        for _ in range(num_registros):
            # Verificar si hay sedes existentes
            if not sedes_disponibles:
                break

            # Seleccionar una sede aleatoria para el EspacioObligado
            sede = random.choice(sedes_disponibles)

            # Crear el EspacioObligado y asociarlo a la sede
            espacio_obligado = EspacioObligado.objects.create(
                estado=random.choice(["CARDIO ASISTIDO CERTIFICADO", "EN PROCESO", "CARDIO ASISTIDO", "CARDIO ASISTIDO CON CERTIFICADO VENCIDO"]),
                motivo=fake.text(),
                sede=sede,
                fecha_creacion=fake.date_between(start_date='-1y', end_date='today')
            )

            # Eliminar la sede seleccionada de las sedes disponibles, 
            # para evitar que se repitan y termine quedando espacios_obligados = sedes con respecto a la cantidad
            sedes_disponibles.remove(sede)

        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {num_registros} registros en la tabla EspacioObligado"))
