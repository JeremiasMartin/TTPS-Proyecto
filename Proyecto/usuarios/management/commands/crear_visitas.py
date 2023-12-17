from django.core.management.base import BaseCommand
from espacios_obligados.models import EspacioObligado, Certificante, Visita
from faker import Faker
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Populate DEA and HistorialDEA data"

    def handle(self, *args, **options):
        cantidad = 1000

        fake = Faker("es_AR")

        espacios_obligados = EspacioObligado.objects.all()
        certificantes = Certificante.objects.all()
        resultados = ["aprobado", "rechazado"]

        for i in range(cantidad):
            espacio_obligado = random.choice(espacios_obligados)
            certificante = random.choice(certificantes)
            fecha_hora = fake.date_between(start_date="-1y", end_date="today")
            observaciones = fake.text(max_nb_chars=200, ext_word_list=None)
            resultado = random.choice(resultados)

            Visita.objects.create(
                espacio_obligado=espacio_obligado,
                certificante=certificante,
                fecha_hora=fecha_hora,
                observaciones=observaciones,
                resultado=resultado,
            )


        self.stdout.write(
            self.style.SUCCESS(
                f"Se generaron y guardaron {cantidad} registros en la tabla Visitas"
            )
        )
