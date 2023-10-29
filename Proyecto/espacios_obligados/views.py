from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.gis.geos import Point
from usuarios.models import Representante
import requests
from django.http import JsonResponse

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
            dea.dea_sede = sede
            dea.save()

            sede.deas_registrados.add(dea)

            return redirect('listar_mis_entidades_sedes')
    else:
        form = DEAForm()
    return render(request, 'dea/registrar_dea.html', {'form': form, 'sede': sede})


def listar_deas(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    deas = DEA.objects.filter(dea_sede=sede)
    return render(request, 'dea/listar_deas.html', {'sede': sede, 'deas': deas})


def editar_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    sede_id = dea.dea_sede.id
    if request.method == 'POST':
        form = DEAEditForm(request.POST, instance=dea)
        if form.is_valid():
            dea = form.save(commit=False)
            dea.save()
            return redirect('listar_deas', sede_id=sede_id)
    else:
        form = DEAEditForm(instance=dea)
    return render(request, 'dea/editar_dea.html', {'form': form, 'sede':sede_id, 'dea': dea})




def verificar_aprobacion_ANMAT(request, dea_id):

    try:
        # Obtén el DEA con el ID especificado
        dea = DEA.objects.get(id=dea_id)

        # URL de la API para obtener la lista de modelos del DEA con el ID especificado
        url = f'https://api.claudioraverta.com/deas/{dea.marca}/modelos/'

        # Realizar una solicitud GET a la API
        response = requests.get(url)

        # Comprobar si la respuesta tiene el código de estado 200 (OK)
        if response.status_code == 200:
            # Analizar la respuesta JSON
            modelos = response.json()
            
            # Verificar si el modelo está en la lista de modelos aprobados por ANMAT
            if any(modelo.get("nombre") == dea.modelo for modelo in modelos):
                # El DEA con el modelo especificado está aprobado por ANMAT
                # Ahora, debes actualizar el campo aprobacion_ANMAT en tu modelo DEA
                
                # Establece el campo aprobacion_ANMAT en True
                dea.aprobacion_ANMAT = True
                dea.save()
                
                return JsonResponse({'success': True})  # Aprobado por ANMAT y campo actualizado

            else:
                return JsonResponse({'success': False, 'message': f'El DEA { dea.marca } { dea.modelo } no está aprobado por ANMAT'})

        else:
            return JsonResponse({'success': False, 'message': f'Error en la solicitud a la API: {response.status_code}'})

    except DEA.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No se encontró el DEA con el ID especificado'})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'success': False, 'message': f'Error en la solicitud a la API: {str(e)}'})
