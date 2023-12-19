from django.core.management.base import BaseCommand
from espacios_obligados.models import DEA, Sede, EspacioObligado
from faker import Faker
import random


class Command(BaseCommand):
    help = "Populate Deas data"

    def handle(self, *args, **options):
        fake = Faker("es_AR")
        deas = [
            {
                "marca": "Meditech",
                "modelos": [
                    "Mempeliece",
                    "Mempeliece",
                    "Venerthagn",
                    "Tamuligusa",
                    "Flaucebato",
                ],
            },
            {
                "marca": "PhisioControl",
                "modelos": [
                    "Gsissidifi",
                    "PhisioControl",
                    "PhisioControl",
                    "PhisioControl",
                    "PhisioControl",
                ],
            },
            {
                "marca": "Medtronic",
                "modelos": [
                    "Colortisol",
                    "Ceciditabe",
                    "Lamunifess",
                    "Sexisquini",
                    "Itergibiqu",
                ],
            },
            {
                "marca": "Mindray",
                "modelos": [
                    "Matinitunt",
                    "Homadertan",
                    "Graessecus",
                    "Auxerehent",
                    "Aedeuntibu",
                ],
            },
            {
                "marca": "HeartSine",
                "modelos": [
                    "Namilcatis",
                    "Appredecta",
                    "Focateneri",
                    "Xansivenat",
                    "Xansivenat",
                ],
            },
            {
                "marca": "Philips",
                "modelos": [
                    "Iuperthagi",
                    "Deberissil",
                    "Herummitio",
                    "Obstisside",
                    "Feluditina",
                ],
            },
            {
                "marca": "Zoll",
                "modelos": [
                    "Focedivast",
                    "Cumperadit",
                    "Cumperadit",
                    "Seraemvill",
                    "Sucuiniust",
                    "Infertinat",
                ],
            },
            {
                "marca": "Defibtech",
                "modelos": [
                    "Emisquissi",
                    "Unumircult",
                    "Geniectorr",
                    "Rogabilien",
                    "Obiquanter",
                ],
            },
        ]

        num_registros = 100

        sedes = Sede.objects.all()

        for _ in range(num_registros):
            dea_data = random.choice(deas)
            sede_asignada = random.choice(sedes)
            modelo = random.choice(dea_data["modelos"])

            dea = DEA.objects.create(
                marca=dea_data["marca"],
                modelo=modelo,
                numero_serie=random.randint(10000000000, 99999999999),
                nombre_representativo=fake.company(),
                solidario=random.choice([True, False]),
                estado=random.choice(["activo", "inactivo"]),
                dea_sede_id=sede_asignada.id,
            )

            # Agregar el DEA a la tabla intermedia deas_registrados
            for espacio_obligado in EspacioObligado.objects.filter(sede=sede_asignada):
                espacio_obligado.sede.deas_registrados.add(dea)

        self.stdout.write(
            self.style.SUCCESS(
                f"Se generaron y guardaron {num_registros} registros en la tabla DEA y se registraron en la tabla intermedia deas_registrados"
            )
        )
