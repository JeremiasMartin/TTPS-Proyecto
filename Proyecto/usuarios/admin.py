from django.contrib import admin
from .models import Provincias, AdminProvincial
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from django.contrib.auth.models import Group

AdminSite.site_url = None

class ClientesAdmin(admin.ModelAdmin):
    search_fields=("nombre","apellido", "telefono", "email")

admin.site.register(Provincias)
admin.site.register(AdminProvincial)