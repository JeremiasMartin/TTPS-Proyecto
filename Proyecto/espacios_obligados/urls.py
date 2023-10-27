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
]
