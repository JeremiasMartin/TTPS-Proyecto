from django.core.management.base import BaseCommand
from espacios_obligados.models import Entidad, Sede, EspacioObligado, DEA
from datawarehouse.models import EntidadDW, SedeDW, EspacioObligadoDW, DEADW

class Command(BaseCommand):
    help = 'Realiza el proceso de ETL para el data warehouse'

    def handle(self, *args, **options):
        # Extract: Obtener datos de la base de datos transaccional
        entidades = Entidad.objects.all()
        sedes = Sede.objects.all()
        espacios_obligados = EspacioObligado.objects.all()
        deas = DEA.objects.all()

        # Transform: Convertir datos y aplicar transformaciones según sea necesario
        for entidad in entidades:
            EntidadDW.objects.create(
                razon_social=entidad.razon_social,
                cuit=entidad.cuit,
                sector=entidad.sector,
                tipo=entidad.tipo
            )

        for sede in sedes:
            SedeDW.objects.create(
                nombre=sede.nombre,
                cant_personas_externas=sede.cant_personas_externas,
                superficie=sede.superficie,
                ubicacion=sede.ubicacion,
                cant_personal=sede.cant_personal,
                direccion=sede.direccion,
                entidad=EntidadDW.objects.get(pk=sede.entidad_id)
            )

        for espacio_obligado in espacios_obligados:
            EspacioObligadoDW.objects.create(
                estado=espacio_obligado.estado,
                sede=SedeDW.objects.get(pk=espacio_obligado.sede_id),
                motivo=espacio_obligado.motivo,
                fecha_creacion=espacio_obligado.fecha_creacion
            )

        for dea in deas:
            DEADW.objects.create(
                marca=dea.marca,
                modelo=dea.modelo,
                numero_serie=dea.numero_serie,
                nombre_representativo=dea.nombre_representativo,
                solidario=dea.solidario,
                estado=dea.estado
            )

        # Load: Guardar los datos transformados en el data warehouse
        self.stdout.write(self.style.SUCCESS('ETL completado con éxito.'))
