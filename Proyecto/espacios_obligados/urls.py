from django.urls import path
from . import views

urlpatterns = [
    path('registrar_entidad/', views.registrar_entidad, name='registrar_entidad'),
    path('registrar_sede/<int:entidad_id>/', views.registrar_sede, name='registrar_sede'),
    path('listar_sedes/<int:entidad_id>/', views.listar_sedes, name='listar_sedes'),
    path('listar_mis_entidades_sedes/', views.listar_mis_entidades_sedes, name='listar_mis_entidades_sedes'),
]
