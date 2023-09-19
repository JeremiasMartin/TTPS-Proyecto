from django.urls import path
from . import views

urlpatterns = [
    path('registro_representante/', views.representante_signup, name='registro_representante'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
