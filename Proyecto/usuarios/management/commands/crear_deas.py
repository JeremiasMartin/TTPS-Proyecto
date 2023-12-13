from django.core.management.base import BaseCommand
from espacios_obligados.models import DEA
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Deas data'

    def handle(self, *args, **options):
        fake = Faker('es_AR')
        deas = [
            {"marca": "Meditech", "modelos": ["Mempeliece", "Mempeliece", "Venerthagn", "Tamuligusa", "Flaucebato"]},
            {"marca": "PhisioControl", "modelos": ["Gsissidifi", "PhisioControl", "PhisioControl", "PhisioControl", "PhisioControl"]},
            {"marca": "Medtronic", "modelos": ["Colortisol", "Ceciditabe", "Lamunifess", "Sexisquini", "Itergibiqu"]},
            {"marca": "Mindray", "modelos": ["Matinitunt", "Homadertan", "Graessecus", "Auxerehent", "Aedeuntibu"]},
            {"marca": "HeartSine", "modelos": ["Namilcatis", "Appredecta", "Focateneri", "Xansivenat", "Xansivenat"]},
            {"marca": "Philips", "modelos": ["Iuperthagi", "Deberissil", "Herummitio", "Obstisside", "Feluditina"]},
            {"marca": "Zoll", "modelos": ["Focedivast", "Cumperadit", "Cumperadit", "Seraemvill", "Sucuiniust", "Infertinat"]},
            {"marca": "Defibtech", "modelos": ["Emisquissi", "Unumircult", "Geniectorr", "Rogabilien", "Obiquanter"]},
        ]

        for dea in deas:
            for modelo in dea["modelos"]:
                DEA.objects.create(
                    marca=dea["marca"],
                    modelo=modelo,
                    numero_serie=random.randint(10000000000, 99999999999),
                    nombre_representativo=fake.name(),
                    solidario=random.choice([True, False]),
                    estado=random.choice(["activo", "inactivo"]),
                    dea_sede_id=random.randint(1, 100)
                )

        self.stdout.write(self.style.SUCCESS(f"Se generaron y guardaron {len(deas)} registros en la tabla DEA"))

