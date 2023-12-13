from django.core.management.base import BaseCommand
from espacios_obligados.models import (
    Sede,
    Representante,
    Responsable,
    Provincias,
    Entidad,
)
from faker import Faker
import random
from django.contrib.gis.geos import Point
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
import time


class Command(BaseCommand):
    help = "Populate Sedes data"
    
    @staticmethod
    def obtener_ciudad_desde_coordenadas(latitud, longitud):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.reverse((latitud, longitud), language="es")

        ciudad = None
        if location and location.address:
            # Buscar la ciudad en diferentes partes de la dirección inversa
            for part in location.address.split(","):
                if "city" in part.lower():
                    ciudad = part.strip()
                    break
            else:
                ciudad = location.address.split(",")[0].strip()

        return ciudad or "Ciudad Desconocida"

    def generar_datos_ubicacion(self):
        # Lista de provincias en Argentina
        provincias = [
            "Buenos Aires",
            "Catamarca",
            "Chaco",
            "Chubut",
            "Córdoba",
            "Corrientes",
            "Entre Ríos",
            "Formosa",
            "Jujuy",
            "La Pampa",
            "La Rioja",
            "Mendoza",
            "Misiones",
            "Neuquén",
            "Río Negro",
            "Salta",
            "San Juan",
            "San Luis",
            "Santa Cruz",
            "Santa Fe",
            "Santiago del Estero",
            "Tierra del Fuego",
            "Tucumán",
        ]

        # Elegir aleatoriamente una provincia
        provincia = random.choice(provincias)

        # Crear una instancia del geocodificador de Nominatim
        geolocator = Nominatim(user_agent="my_app")

        # Obtener información de geolocalización para la provincia
        location = geolocator.geocode(f"{provincia}, Argentina", language="es")

        # Extraer información relevante
        ciudad = self.obtener_ciudad_desde_coordenadas(location.latitude, location.longitude)
        direccion = f"{ciudad}, {provincia}"
        latitud = location.latitude if location else 0.0
        longitud = location.longitude if location else 0.0

        # Crear un objeto Point
        ubicacion = Point(longitud, latitud)

        return provincia, direccion, ubicacion

    def handle(self, *args, **options):
        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx
        fake = Faker("es_AR")
        num_registros = 100

        representantes = Representante.objects.all()


        for _ in range(num_registros):
            provincia, direccion, ubicacion = self.generar_datos_ubicacion()
            time.sleep(2)

            sede = Sede.objects.create(
                nombre=fake.company(),
                cant_personas_externas=random.randint(1, 100),
                superficie=random.randint(1, 100),
                ubicacion=ubicacion,
                cant_personal=random.randint(1, 500),
                direccion=direccion,
                personal_capacitado=bool(random.getrandbits(1)),
                senaletica=bool(random.getrandbits(1)),
                protocolo_accion=bool(random.getrandbits(1)),
                sistema_emergencia=bool(random.getrandbits(1)),
                deas_decreto=random.randint(1, 3),
                provincia=Provincias.objects.get(nombre=provincia),
                entidad=Entidad.objects.create(
                    razon_social=fake.company(),
                    cuit=random.randint(10000000000, 99999999999),
                    sector=random.choice(["publica", "privada"]),
                    tipo=random.choice(
                        [
                            "Administracion Publica",
                            "Entidad Financiera",
                            "Institución educativa",
                            "Institucion Recreativa",
                            "Institucion de Salud",
                        ]
                    ),
                ),
            )
            sede.representantes.add(random.choice(representantes))

            sede.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Se generaron y guardaron {num_registros} registros en la tabla Sede"
            )
        )
