from .views import ejecutar_etl
from django.urls import path

urlpatterns = [
    path('ejecutar_etl/', ejecutar_etl, name='ejecutar_etl'),
]