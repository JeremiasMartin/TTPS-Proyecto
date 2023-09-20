from django.urls import path
from . import views

urlpatterns = [
    path('registro_representante/', views.representante_signup, name='registro_representante'),
    path('perfil_representante/', views.perfil_representante, name='perfil_representante'),
    path('editar_perfil_representante/', views.editar_perfil_representante, name='editar_perfil_representante'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
