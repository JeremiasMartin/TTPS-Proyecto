from django.urls import path
from . import views
import threading

urlpatterns = [
    path('registrar_entidad/', views.registrar_entidad, name='registrar_entidad'),
    path('registrar_sede/<int:entidad_id>/',
         views.registrar_sede, name='registrar_sede'),
    path('listar_sedes/<int:entidad_id>/',
         views.listar_sedes, name='listar_sedes'),
    path('listar_mis_entidades_sedes/', views.listar_mis_entidades_sedes,
         name='listar_mis_entidades_sedes'),
    path('administrar_entidad_sede/<int:sede_id>/',
         views.administrar_entidad_sede, name='administrar_entidad_sede'),
    path('editar_sede/<int:sede_id>/', views.editar_sede, name='editar_sede'),
    path('declaracion_jurada/<int:sede_id>/',
         views.declaracion_jurada, name='declaracion_jurada'),
    path('registrar_dea/<int:sede_id>/',
         views.registrar_dea, name='registrar_dea'),
    path('cargar_modelos/', views.cargar_modelos, name='cargar_modelos'),
    path('listar_deas/<int:sede_id>/', views.listar_deas, name='listar_deas'),
    path('editar_dea/<int:dea_id>/', views.editar_dea, name='editar_dea'),
    path('activar_dea/<int:dea_id>/', views.activar_dea, name='activar_dea'),
    path('desactivar_dea/<int:dea_id>/', views.desactivar_dea, name='desactivar_dea'),
    path('eliminar_dea/<int:dea_id>/', views.eliminar_dea, name='eliminar_dea'),
    path('mapa/', views.listar_deas_activos, name='mapa'),
    path('mapa_solidario/', views.listar_deas_activos_solidarios, name='mapa_solidario'),
    path('notificar_responsables/<int:sede_id>/', views.notificar_responsables, name='notificar_responsables'),
    path('registrar_servicio_dea/<int:dea_id>/', views.registrar_servicio_dea, name='registrar_servicio_dea'),
    path('listar_reparaciones_dea/<int:dea_id>/', views.listar_reparaciones_dea, name='listar_reparaciones_dea'),
    path('listar_mantenimientos_dea/<int:dea_id>/', views.listar_mantenimientos_dea, name='listar_mantenimientos_dea'),
    path('registrar_responsable/<int:sede_id>/', views.registrar_responsable, name='registrar_responsable'),
    path('listar_responsables/<int:sede_id>/', views.listar_responsables, name='listar_responsables'),
    path('editar_responsable/<int:responsable_id>/', views.editar_responsable, name='editar_responsable'),
    path('eliminar_responsable/<int:responsable_id>/', views.eliminar_responsable, name='eliminar_responsable'),
    path('solicitud_aprobacion/', views.solicitud_aprobacion, name='solicitud_aprobacion'),
    path('solicitud_aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('lista_solicitudes_pendientes/', views.lista_solicitudes_pendientes, name='lista_solicitudes_pendientes'),
    path('aprobar_solicitud/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('rechazar_solicitud/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),

     # Certificante
    path('certificante/listado_espacios_obligados', views.listar_espacios_obligados_certificante,
         name='listar_espacios_obligados_certificante'),
     path('certificante/nueva-visita/<int:espacio_obligado_id>', views.nueva_visita, name='nueva_visita'),
     path('certificante/visitas/espacio-obligado/<int:espacio_obligado_id>', views.listar_visitas, name='listar_visitas'),
     path('certificante/visita/<int:visita_id>', views.eliminar_visita, name='eliminar_visita'),


     # Muerte Subita
     path('registrar_muerte_subita/<int:sede_id>/', views.registrar_muerte_subita, name='registrar_muerte_subita'),
     path('listar_eventos_muerte_subita/<int:sede_id>/', views.listar_eventos_muerte_subita, name='listar_eventos_muerte_subita'),
]


# Iniciar el hilo que ejecuta el planificador al iniciar la aplicación (chequeo de vencimiento de ertificaciones)
threading.Thread(target=views.run_scheduler, daemon=True).start()