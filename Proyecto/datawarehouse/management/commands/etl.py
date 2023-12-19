from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from datawarehouse.models import (
    DimFechaLog,
    DimFechaCreacion,
    DimFechaEventoMS,
    DimEstado,
    DimSede,
    DimLugar,
    DimDEA,
    DimMuerteSubita,
    Hechos,
)
from espacios_obligados.models import EspacioObligado, Sede, DEA, EventoMuerteSubita
import random


class Command(BaseCommand):
    help = "Run the ETL process to populate the data warehouse models."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting ETL process..."))

        # Call the ETL function
        run_etl()

        self.stdout.write(self.style.SUCCESS("ETL process completed successfully."))


@transaction.atomic
def run_etl():
    print("Limpiando data warehouse...")
    DimFechaLog.objects.all().delete()
    DimFechaCreacion.objects.all().delete()
    DimFechaEventoMS.objects.all().delete()
    DimEstado.objects.all().delete()
    DimSede.objects.all().delete()
    DimLugar.objects.all().delete()
    DimDEA.objects.all().delete()
    DimMuerteSubita.objects.all().delete()
    Hechos.objects.all().delete()

    # Crear función para cargar DimFechaCreacion
    def cargar_dim_fecha_creacion(fecha):
        print(f"Cargando DimFechaCreacion para fecha: {fecha}")
        return DimFechaCreacion.objects.create(
            dia=fecha.day,
            mes=fecha.month,
            anho=fecha.year,
        )

    # Crear función para cargar DimFechaEventoMS
    def cargar_dim_fecha_evento(fecha):
        print(f"Cargando DimFechaEventoMS para fecha: {fecha}")
        dim_fecha_evento = DimFechaEventoMS.objects.create(
            dia=fecha.day,
            mes=fecha.month,
            anho=fecha.year,
        )
        return dim_fecha_evento, None

    # Crear función para cargar DimLugar
    def cargar_dim_lugar(sede):
        direccion_parts = sede.direccion.split(", ")
        ciudad = direccion_parts[0]
        provincia = direccion_parts[1]
        print(f"Cargando DimLugar para ciudad: {ciudad}, provincia: {provincia}")
        return DimLugar.objects.create(
            provincia=provincia,
            ciudad=ciudad,
        )


    # Crear función para cargar DimMuerteSubita
    def cargar_dim_muerte_subita(evento, dim_sede):
        dim_fecha_evento, _ = cargar_dim_fecha_evento(evento.fecha)

        gender_mapping = {"masculino": "M", "femenino": "F", "otro": "O"}
        sexo_mapped = gender_mapping.get(evento.sexo.lower(), "otro")

        # Crear o buscar DimDEA si se utilizó un DEA
        dea_instance = None
        if evento.dea:
            try:
                dea_instance = DimDEA.objects.get(
                    marca=evento.dea.marca,
                    modelo=evento.dea.modelo,
                    idSede=dim_sede,
                )
            except DimDEA.MultipleObjectsReturned:
                # Si se encuentran múltiples objetos, elegir uno arbitrariamente
                dea_instance = DimDEA.objects.filter(
                    marca=evento.dea.marca,
                    modelo=evento.dea.modelo,
                    idSede=dim_sede,
                ).first()
            except DimDEA.DoesNotExist:
                # Si no existe, crear una nueva instancia
                dea_instance = DimDEA.objects.create(
                    marca=evento.dea.marca,
                    modelo=evento.dea.modelo,
                    idSede=dim_sede,
                )

        DimMuerteSubita.objects.create(
            sexo=sexo_mapped,
            edad=evento.edad,
            idSede=dim_sede,
            idFecha=dim_fecha_evento,
            inSitu=evento.fallecido,
            dea=dea_instance,
        )

        print(f"DEA Instance: {dea_instance}")

    # Cargar datos en el data warehouse
    for espacio_obligado in EspacioObligado.objects.all():
        dim_sede = None
        dim_estado = None
        try:
            # Cargar DimFechaCreacion
            creacion = cargar_dim_fecha_creacion(espacio_obligado.fecha_creacion)

            # Cargar DimLugar
            dim_lugar = cargar_dim_lugar(espacio_obligado.sede)

            # Cargar DimSede
            dim_sede, _ = DimSede.objects.get_or_create(
                tipo=espacio_obligado.sede.entidad.tipo,
                fecha_creacion=creacion,
                idLugar=dim_lugar,
                idEstado=dim_estado,
            )

            # Cargar DimEstado
            dim_estado, _ = DimEstado.objects.get_or_create(
                nombreEstado=espacio_obligado.estado,
                fecha_creacion=DimFechaLog.objects.create(
                    dia=random.randint(1, 28),
                    mes=random.randint(1, 12),
                    anho=random.randint(2015, 2023),
                ),
                idSede=dim_sede,
            )

            # Cargar DimDEA
            for dea in DEA.objects.filter(sede=espacio_obligado.sede):
                DimDEA.objects.create(
                    marca=dea.marca,
                    modelo=dea.modelo,
                    idSede=dim_sede,
                )

            # Cargar DimMuerteSubita
            for evento in EventoMuerteSubita.objects.filter(
                sede_id=espacio_obligado.sede.id
            ):
                cargar_dim_muerte_subita(evento, dim_sede)

            # Calcular métricas para Hechos
            cant_espacios_obligados = EspacioObligado.objects.filter(
                sede=espacio_obligado.sede
            ).count()
            cant_deas = DEA.objects.filter(sede=espacio_obligado.sede).count()
            cant_deas_solidarios = DEA.objects.filter(
                sede=espacio_obligado.sede, solidario=True
            ).count()
            cant_muertes_subitas = EventoMuerteSubita.objects.filter(
                sede_id=espacio_obligado.sede.id
            ).count()
            cant_muertes_in_situ = EventoMuerteSubita.objects.filter(
                sede_id=espacio_obligado.sede.id, fallecido=True
            ).count()

            # Cargar Hechos con las métricas calculadas
            Hechos.objects.create(
                idEstado=dim_estado,
                idLugar=dim_lugar,
                idSede=dim_sede,
                cantEspaciosObligados=cant_espacios_obligados,
                cantDeas=cant_deas,
                cantDEAsSolidarios=cant_deas_solidarios,
                cantMuertesSubitas=cant_muertes_subitas,
                cantMuertesInSitu=cant_muertes_in_situ,
            )
        except IntegrityError as e:
            print(
                f"Error al cargar datos para EspacioObligado ID {espacio_obligado.id}: {e}"
            )


if __name__ == "__main__":
    run_etl()
