from django.shortcuts import render, redirect
from .models import Entidad, Sede, Provincias
from .forms import EntidadForm, SedeForm

# Create your views here.

def registrar_entidad(request):
    entidades = Entidad.objects.all()
    if request.method == 'POST':
        form = EntidadForm(request.POST)
        if form.is_valid():
            entidad = form.save()
            return redirect('registrar_sede', entidad_id=entidad.id)
    else:
        form = EntidadForm()
    return render(request, 'entidad/registrar_entidad.html', {'form': form, 'entidades': entidades})

def registrar_sede(request, entidad_id):
    entidad = Entidad.objects.get(id=entidad_id)
    sedes = Sede.objects.filter(entidad=entidad)
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            sede = form.save(commit=False)
            sede.entidad = entidad
            sede.representantes = request.user.representante
            sede.save()
            return redirect('listar_sedes', entidad_id=entidad.id)
    else:
        form = SedeForm()
    provincias = Provincias.objects.all()
    return render(request, 'sede/registrar_sede.html', {'form': form, 'entidad': entidad, 'sedes': sedes, 'provincias': provincias})

def listar_sedes(request, entidad_id):
    entidad = Entidad.objects.get(id=entidad_id)
    sedes = Sede.objects.filter(entidad=entidad)
    return render(request, 'sede/listar_sedes.html', {'entidad': entidad, 'sedes': sedes})


def listar_mis_entidades_sedes(request):

    representante = request.user.representante

    entidades_sedes = Sede.objects.filter(representantes=representante)

    return render(request, 'listar_mis_entidades_sedes.html', {'entidades_sedes': entidades_sedes})


