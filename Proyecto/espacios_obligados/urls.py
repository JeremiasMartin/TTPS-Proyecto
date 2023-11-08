from django.urls import path
from . import views

urlpatterns = [
    path('registrar_entidad/', views.registrar_entidad, name='registrar_entidad'),
    path('registrar_sede/<int:entidad_id>/', views.registrar_sede, name='registrar_sede'),
    path('listar_sedes/<int:entidad_id>/', views.listar_sedes, name='listar_sedes'),
    path('listar_mis_entidades_sedes/', views.listar_mis_entidades_sedes, name='listar_mis_entidades_sedes'),
    path('administrar_entidad_sede/<int:sede_id>/', views.administrar_entidad_sede, name='administrar_entidad_sede'),
    path('editar_sede/<int:sede_id>/', views.editar_sede, name='editar_sede'),
    path('declaracion_jurada/<int:sede_id>/', views.declaracion_jurada, name='declaracion_jurada'),
    path('registrar_dea/<int:sede_id>/', views.registrar_dea, name='registrar_dea'),
    path('cargar_modelos/', views.cargar_modelos, name='cargar_modelos'),
    path('listar_deas/<int:sede_id>/', views.listar_deas, name='listar_deas'),
    path('editar_dea/<int:dea_id>/', views.editar_dea, name='editar_dea'),
    path('eliminar_dea/<int:dea_id>/', views.eliminar_dea, name='eliminar_dea'),
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

]
