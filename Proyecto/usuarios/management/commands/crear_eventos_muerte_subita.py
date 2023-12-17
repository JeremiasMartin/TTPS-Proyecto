from django.core.management.base import BaseCommand
from espacios_obligados.models import EventoMuerteSubita, Sede, Representante, DEA
from faker import Faker
import random


class Command(BaseCommand):
    help = "Populate EventoMuerteSubita data"

    def handle(self, *args, **options):
        fake = Faker("es_AR")
        num_registros = 100

        for _ in range(num_registros):
            sede = random.choice(Sede.objects.all())
            representante = random.choice(sede.representantes.all())

            # Simular si se utilizó un DEA o no
            dea_utilizado = random.choice([True, False])
            dea_obj = (
                random.choice(DEA.objects.filter(dea_sede=sede))
                if (dea_utilizado and DEA.objects.filter(dea_sede=sede).exists())
                else None
            )

            # Simular si se realizó RCP o no
            rcp_realizado = random.choice([True, False])

            # Simular valores de descarga eléctrica solo si se utilizó un DEA
            descarga_electrica = random.choice([True, False]) if dea_utilizado else None
            cantidad_descarga = random.randint(1, 10) if descarga_electrica else None

            # Simular valores de tiempo de RCP solo si se realizó RCP
            tiempo_rcp = random.randint(1, 30) if rcp_realizado else None

            evento = EventoMuerteSubita.objects.create(
                fecha=fake.date_between(start_date="-1y", end_date="today"),
                sexo=random.choice(["masculino", "femenino", "otro"]),
                edad=random.randint(18, 90),
                fallecido=random.choice([True, False]),
                rcp=rcp_realizado,
                tiempo_rcp=tiempo_rcp,
                dea=dea_obj,
                inconveniente=fake.text(max_nb_chars=250)
                if random.choice([True, False])
                else None,
                descarga_electrica=descarga_electrica,
                cantidad_descarga=cantidad_descarga,
                observaciones=fake.text(max_nb_chars=250)
                if random.choice([True, False])
                else None,
                sede_id=sede,
                representante_id=representante,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Se generaron y guardaron {num_registros} registros en la tabla EventoMuerteSubita"
            )
        )
