from django.urls import path
from ProyectoApp.views import *

urlpatterns = [
    path('', home, name="Home"),
]