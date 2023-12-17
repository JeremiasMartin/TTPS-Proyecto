from django.core.management.base import BaseCommand
from espacios_obligados.models import DEA, HistorialDEA
from faker import Faker
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Populate DEA and HistorialDEA data"

    def handle(self, *args, **options):
        cantidad = 1000

        fake = Faker("es_AR")

        deas = DEA.objects.all()

        tipos_servicio = ["Reparación", "Mantenimiento"]

        for i in range(cantidad):
            dea = random.choice(deas)
            dia = fake.date_between(start_date="-1y", end_date="today")
            servicio = random.choice(tipos_servicio)
            observaciones = fake.text(max_nb_chars=200, ext_word_list=None)

            HistorialDEA.objects.create(
                dea=dea,
                dia=dia,
                servicio=servicio,
                observaciones=observaciones,
            )


        self.stdout.write(
            self.style.SUCCESS(
                f"Se generaron y guardaron {cantidad} registros en la tabla Historial DEA"
            )
        )
