from django.urls import path, include
from ProyectoApp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name="Home")
]
