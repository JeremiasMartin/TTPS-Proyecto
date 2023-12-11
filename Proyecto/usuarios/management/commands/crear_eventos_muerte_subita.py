from django.core.management.base import BaseCommand
from espacios_obligados.models import EventoMuerteSubita, Sede, Representante
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate EventoMuerteSubita data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        num_registros = 1

        for _ in range(num_registros):
            sede = random.choice(Sede.objects.all())
            representante = random.choice(sede.representantes.all())  # Selecciona un representante de la sede

            evento = EventoMuerteSubita.objects.create(
                fecha=fake.date_between(start_date='-1y', end_date='today'),
                sexo=random.choice(['masculino', 'femenino', 'otro']),
                edad=random.randint(18, 90),
                fallecido=random.choice([True, False]),
                rcp=random.choice([True, False]),
                tiempo_rcp=random.randint(1, 30) if random.choice([True, False]) else None,
                dea=random.choice([True, False]),
                inconveniente=fake.text(max_nb_chars=250) if random.choice([True, False]) else None,
                descarga_electrica=random.choice([True, False]) if random.choice([True, False]) else None,
                cantidad_descarga=random.randint(1, 10) if random.choice([True, False]) else None,
                observaciones=fake.text(max_nb_chars=250) if random.choice([True, False]) else None,
                sede_id=sede,
                representante_id=representante
            )

        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {num_registros} registros en la tabla EventoMuerteSubita"))
