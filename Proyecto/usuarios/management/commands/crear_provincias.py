from django.core.management.base import BaseCommand
from espacios_obligados.models import Provincias
import random

class Command(BaseCommand):
    help = 'Populate Provincias data'

    def handle(self, *args, **options):
        provincias = [
            "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", 
            "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa",
            "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro",
            "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe",
            "Santiago del Estero", "Tierra del Fuego", "Tucumán"
        ]

        for provincia in provincias:
            Provincias.objects.create(nombre=provincia, validez_certificado=5)

        self.stdout.write(
            self.style.SUCCESS(f'Se crearon y guardaron las provincias en la tabla Provincias')
        )
