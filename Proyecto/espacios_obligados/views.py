from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.gis.geos import Point
from usuarios.models import Representante
import requests
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

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

    # Realiza una solicitud a la API para obtener las marcas disponibles
    url = 'https://api.claudioraverta.com/deas/'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            marcas = [{'id': dea['id'], 'marca': dea['marca']} for dea in response.json()]
        else:
            marcas = []

    except requests.exceptions.RequestException as e:
        print(f'Error en la solicitud a la API: {str(e)}')
        marcas = []

    if request.method == 'POST':
        form = DEAForm(request.POST)
        if form.is_valid():
            dea = form.save(commit=False)
            marca_id = request.POST.get('marca')
            marca_nombre = None
            
            for marca in marcas:
                if str(marca['id']) == str(marca_id):
                    marca_nombre = marca['marca']
                    break
            dea.marca = marca_id if marca_nombre is None else marca_nombre
            dea.dea_sede = sede
            dea.save()
            sede.deas_registrados.add(dea)
            return redirect('listar_deas', sede_id=sede.id)

    else:
        form = DEAForm()

    return render(request, 'dea/registrar_dea.html', {'form': form, 'sede': sede, 'marcas': marcas})



def cargar_modelos(request):
    marca_seleccionada = request.POST.get('marca', None)
    if marca_seleccionada:
        url = f'https://api.claudioraverta.com/deas/{marca_seleccionada}/modelos/'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                modelos = [modelo['nombre'] for modelo in response.json()]
            else:
                modelos = []

        except requests.exceptions.RequestException as e:
            print(f'Error en la solicitud a la API: {str(e)}')
            modelos = []
    else:
        modelos = []

    return JsonResponse({'modelos': modelos})





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



    
def eliminar_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    sede_id = dea.dea_sede.id
    if request.method == 'POST':
        dea.delete()
        return redirect('listar_deas', sede_id=sede_id)
    return render(request, 'dea/eliminar_dea.html', {'dea': dea, 'sede': sede_id})

def registrar_servicio_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    sede = dea.dea_sede
    if request.method == 'POST':
        form = DEAServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.dea = dea
            servicio.save()
            return redirect('listar_deas', sede_id=dea.dea_sede.id)
    else:
        form = DEAServicioForm()
    return render(request, 'dea/registrar_servicio_dea.html', {'form': form, 'dea': dea, 'sede': sede})


def listar_reparaciones_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    sede = dea.dea_sede
    reparaciones = HistorialDEA.objects.filter(dea=dea, servicio='Reparación')
    return render(request, 'dea/listar_reparaciones.html', {'dea': dea, 'reparaciones': reparaciones, 'sede': sede})

def listar_mantenimientos_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    sede = dea.dea_sede
    mantenimientos = HistorialDEA.objects.filter(dea=dea, servicio='Mantenimiento')
    return render(request, 'dea/listar_mantenimientos.html', {'dea': dea, 'mantenimientos': mantenimientos, 'sede': sede})



def registrar_responsable(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    if request.method == 'POST':
        form = ResponsableForm(request.POST)
        if form.is_valid():
            responsable = form.save(commit=False)
            responsable.sede_asignada = sede
            responsable.save()
            sede.responsables.add(responsable)
            return redirect('listar_mis_entidades_sedes')
    else:
        form = ResponsableForm()
    return render(request, 'responsable/registrar_responsable.html', {'form': form, 'sede': sede})

def listar_responsables(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    responsables = Responsable.objects.filter(sede_asignada=sede)
    return render(request, 'responsable/listar_responsables.html', {'sede': sede, 'responsables': responsables})

def editar_responsable(request, responsable_id):
    responsable = Responsable.objects.get(id=responsable_id)
    sede_id = responsable.sede_asignada.id
    if request.method == 'POST':
        form = ResponsableForm(request.POST, instance=responsable)
        if form.is_valid():
            responsable = form.save(commit=False)
            responsable.save()
            return redirect('listar_responsables', sede_id=sede_id)
    else:
        form = ResponsableForm(instance=responsable)
    return render(request, 'responsable/editar_responsable.html', {'form': form, 'sede': sede_id, 'responsable': responsable})

def eliminar_responsable(request, responsable_id):
    responsable = Responsable.objects.get(id=responsable_id)
    sede_id = responsable.sede_asignada.id
    if request.method == 'POST':
        responsable.delete()
        return redirect('listar_responsables', sede_id=sede_id)
    return render(request, 'responsable/eliminar_responsable.html', {'responsable': responsable, 'sede': sede_id})

def solicitud_aprobacion(request):
    show_alert = False
    show_submit_alert = True
    if request.method == 'POST':
        form = SolicitudAprobacionForm(request.POST)
        if form.is_valid():
            representante = request.user.representante
            entidad = form.cleaned_data['entidad']
            sede = form.cleaned_data['sede']
            motivo = form.cleaned_data['motivo']
            
            # Verificar si ya existe una solicitud con la misma entidad y sede
            if SolicitudAprobacion.objects.filter(entidad=entidad, sede=sede).exists():
                # Mostrar un mensaje de error
                show_alert = True
                show_submit_alert=False
                messages.error(request, 'Ya has solicitado para esta entidad y sede.')
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'show_alert': show_alert, 'show_submit_alert': show_submit_alert})
            
            solicitud_aprobacion = SolicitudAprobacion(
                representante=representante, 
                entidad=entidad, 
                sede=sede, 
                motivo=motivo
            )
            solicitud_aprobacion.save() 
            return redirect('/dash')
            
    else:
        form = SolicitudAprobacionForm()

    return render(request, 'solicitud_aprobacion.html', {'form': form, 'show_alert': show_alert, 'show_submit_alert': True})



def lista_solicitudes_pendientes(request):   

    solicitudes_pendientes = SolicitudAprobacion.objects.filter(aprobado=False)
    return render(request, 'lista_solicitudes_pendientes.html', {'solicitudes_pendientes': solicitudes_pendientes})

def aprobar_solicitud(request, solicitud_id):
    if not request.user.is_authenticated or not request.user.adminprovincial:
        return HttpResponseForbidden("No tienes permisos para realizar esta acción.")
    
    solicitud = get_object_or_404(SolicitudAprobacion, pk=solicitud_id)
    solicitud.aprobado = True
    solicitud.aprobado_por = request.user.adminprovincial
    solicitud.save()
    return redirect('lista_solicitudes_pendientes')

def rechazar_solicitud(request, solicitud_id):
    if not request.user.is_authenticated or not request.user.adminprovincial:
        return HttpResponseForbidden("No tienes permisos para realizar esta acción.")
    
    solicitud = get_object_or_404(SolicitudAprobacion, pk=solicitud_id)
    solicitud.aprobado = False

    solicitud.save()
    return redirect('lista_solicitudes_pendientes')