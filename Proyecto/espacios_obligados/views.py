from django.shortcuts import render, redirect
from .models import Entidad, Sede, Provincias
from .forms import EntidadForm, SedeForm, EditSedeForm, DeclaracionJuradaForm, DEAForm
from django.contrib.gis.geos import Point
from usuarios.models import Representante

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
            coordenadas = request.POST.get('ubicacion')  # Obtiene el valor de la ubicación del campo oculto
            if coordenadas:
                coordenadas_list = coordenadas.split(',')
                if len(coordenadas_list) == 2:
                    latitud, longitud = coordenadas_list
                    sede.ubicacion = Point(float(longitud), float(latitud))
            representante = Representante.objects.get(user=request.user)
            sede.save()  # Guarda la sede primero
            sede.representantes.add(representante)  # Agrega representantes después de guardar la sede
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


def administrar_entidad_sede(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    return render(request, 'administrar_entidad_sede.html', {'sede': sede})


def editar_sede(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    if request.method == 'POST':
        form = EditSedeForm(request.POST, instance=sede)
        if form.is_valid():
            sede = form.save(commit=False)
            coordenadas = form.cleaned_data.get('ubicacion')
            if coordenadas:
                latitud = coordenadas.y
                longitud = coordenadas.x
                sede.ubicacion = Point(longitud, latitud)
            sede.save()

            return redirect('listar_mis_entidades_sedes')
    else:
        form = EditSedeForm(instance=sede)
    return render(request, 'sede/editar_sede.html', {'form': form, 'sede': sede})


def declaracion_jurada(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    if request.method == 'POST':
        form = DeclaracionJuradaForm(request.POST, instance=sede)
        if form.is_valid():
            ddjj = form.save(commit=False)
            ddjj.save()
            return redirect('listar_mis_entidades_sedes')
    else:
        form = DeclaracionJuradaForm(instance=sede)
    return render(request, 'sede/declaracion_jurada.html', {'form': form, 'sede': sede})



def registrar_dea(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    if request.method == 'POST':
        form = DEAForm(request.POST)
        if form.is_valid():
            dea = form.save(commit=False)
            dea.sede = sede
            dea.save()

            sede.deas_registrados.add(dea)

            return redirect('listar_mis_entidades_sedes')
    else:
        form = DEAForm()
    return render(request, 'sede/registrar_dea.html', {'form': form, 'sede': sede})
