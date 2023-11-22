from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.gis.geos import Point
from usuarios.models import Representante, Certificante
import requests
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.conf import settings
from django.db.models import Q

# Create your views here.


def registrar_entidad(request):
    entidades = Entidad.objects.all()
    if request.method == 'POST':
        form = EntidadForm(request.POST)
        if form.is_valid():
            cuit = form.cleaned_data['cuit']
            try:
                entidad = Entidad.objects.filter(cuit=cuit).first() # si ya existe solo pasa la primera entidady pasa a guardar sede
                return redirect('registrar_sede', entidad_id=entidad.id)
            except :
                print("La entidad no existe.")# si no existe solo guarda y pasa a la sede
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
            # Obtiene el valor de la ubicación del campo oculto
            coordenadas = request.POST.get('ubicacion')
            if coordenadas:
                coordenadas_list = coordenadas.split(',')
                if len(coordenadas_list) == 2:
                    latitud, longitud = coordenadas_list
                    sede.ubicacion = Point(float(longitud), float(latitud))
            representante = Representante.objects.get(user=request.user)
            try:
                if sede_y_direccion_ya_existe(sede.nombre, sede.direccion,sede.entidad.id):
                    if representante_ya_existe_en_sede(sede.nombre,representante):
                        ##-->si el representante ya existe para la sede se muestra un error
                        messages.warning(request, 'Este representante ya está asociado a esta sede.')
                        return redirect('registrar_sede', entidad_id=entidad_id)
                    else:
                        try:
                            sede_existente = Sede.objects.filter(nombre=sede.nombre, direccion=sede.direccion).first()
                        except MultipleObjectsReturned:
                            print("Hay múltiples sedes con el mismo nombre y dirección.")
                        nueva_solicitud=SolicitudAprobacion.objects.create(
                            representante=representante,
                            entidad=entidad,
                            sede=sede_existente,
                            motivo="Autogenerado por sistema"  # Reemplaza con el motivo real
                        )
                        nueva_solicitud.save()
                else:
                    sede.save()  # Guarda la sede primero #la sede no existe entonces guarda
                    # Agrega representantes después de guardar la sede
                    sede.representantes.add(representante)
                #la sede existe entonces no la guarda
            except Exception as e:
                 print(f"Error: {e}")

            return redirect('listar_sedes', entidad_id=entidad.id)
    else:
        form = SedeForm()
    provincias = Provincias.objects.all()
    return render(request, 'sede/registrar_sede.html', {'form': form, 'entidad': entidad, 'sedes': sedes, 'provincias': provincias})

def sede_y_direccion_ya_existe(nombre, direccion,entidad_id):
    try:
        # Verifica si ya existe una sede con el mismo nombre y dirección
        Sede.objects.get(nombre=nombre, direccion=direccion, entidad_id=entidad_id)
        return True
    except ObjectDoesNotExist:
        return False
    
def representante_ya_existe_en_sede(nombre_sede,representante):
    try:
        sede = Sede.objects.get(nombre=nombre_sede)
    except Sede.DoesNotExist:
        return False

    return sede.representantes.filter(pk=representante.pk).exists()

def listar_sedes(request, entidad_id):
    entidad = Entidad.objects.get(id=entidad_id)
    sedes = Sede.objects.filter(entidad=entidad)
    return render(request, 'sede/listar_sedes.html', {'entidad': entidad, 'sedes': sedes})


def listar_mis_entidades_sedes(request):

    representante = request.user.representante

    entidades_sedes = Sede.objects.filter(representantes=representante)

    sedes_aprobadas = EspacioObligado.objects.filter(sede__in=entidades_sedes).exclude(estado='RECHAZADO') # Capturo las sedes que hayan sido aprobadas (ya son espacios obligados) y su estado no sea "Rechazado"

    return render(request, 'listar_mis_entidades_sedes.html', {'entidades_sedes': sedes_aprobadas})


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
            sede_espacio = EspacioObligado.objects.get(sede=sede) # Capturo el espacio obligado para poder modificar su estado si la ddjj está aprobada
            deas = DEA.objects.filter(dea_sede=sede) # Capturo los deas registrados de la sede para chequear si coinciden con lo declarado en la ddjj
            if ((ddjj.personal_capacitado and ddjj.senaletica and ddjj.protocolo_accion and ddjj.sistema_emergencia) and ddjj.deas_decreto <= len(deas)):
                sede_espacio.estado = "CARDIO ASISTIDO"
            else:
                sede_espacio.estado = "EN PROCESO"
            sede_espacio.save()
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
            marcas = [{'id': dea['id'], 'marca': dea['marca']}
                      for dea in response.json()]
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

            deas = DEA.objects.filter(dea_sede=sede) # Capturo los deas registrados de la sede para chequear si coinciden con lo declarado en la ddjj
            sede_espacio = EspacioObligado.objects.get(sede=sede) # Capturo el espacio obligado para poder modificar su estado si la ddjj está aprobada
            # Chequeo que la cantidad de deas registrados coincida con la cantidad declarada en la ddjj
            if ((sede.personal_capacitado and sede.senaletica and sede.protocolo_accion and sede.sistema_emergencia) and sede.deas_decreto <= len(deas)):
                sede_espacio.estado = "CARDIO ASISTIDO"
                sede_espacio.save()


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
    return render(request, 'dea/editar_dea.html', {'form': form, 'sede': sede_id, 'dea': dea})


def activar_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    dea.estado = 'activo'
    dea.save()
    return redirect('listar_deas', sede_id=dea.dea_sede.id)

def desactivar_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    dea.estado = 'inactivo'
    dea.save()
    return redirect('listar_deas', sede_id=dea.dea_sede.id)
    
def eliminar_dea(request, dea_id):
    dea = DEA.objects.get(id=dea_id)
    sede_id = dea.dea_sede.id
    if request.method == 'POST':
        dea.delete()

        deas = DEA.objects.filter(dea_sede__id=sede_id) # Capturo los deas registrados de la sede para chequear si coinciden con lo declarado en la ddjj
        sede_espacio = EspacioObligado.objects.get(sede__id=sede_id) # Capturo el espacio obligado para poder modificar su estado si la ddjj está aprobada
        # Chequeo que la cantidad de deas registrados coincida con la cantidad declarada en la ddjj
        if((sede_espacio.sede.personal_capacitado and sede_espacio.sede.senaletica and sede_espacio.sede.protocolo_accion and sede_espacio.sede.sistema_emergencia) and sede_espacio.sede.deas_decreto <= len(deas)):
            sede_espacio.estado = "CARDIO ASISTIDO"
        else:
            sede_espacio.estado = "EN PROCESO"
        sede_espacio.save()
        

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
    mantenimientos = HistorialDEA.objects.filter(
        dea=dea, servicio='Mantenimiento')
    return render(request, 'dea/listar_mantenimientos.html', {'dea': dea, 'mantenimientos': mantenimientos, 'sede': sede})


def listar_deas_activos(request):
    deas = DEA.objects.filter(estado='activo')
    return render(request, 'mapa.html', {'deas': deas})


def listar_deas_activos_solidarios(request): 
    # Filtrar las sedes que tienen DEAs activos y solidarios
    sedes = Sede.objects.filter(deas_registrados__estado='activo', deas_registrados__solidario=True).distinct()
    return render(request, 'mapa_deas_solidarios.html', {'sedes': sedes})


def notificar_responsables(request, sede_id):
    print(f"Llamada a notificar_responsables con sede_id={sede_id}")
    sede = Sede.objects.get(id=sede_id)
    responsables = sede.responsables.all()
    # Definir el asunto, remitente, y demás detalles del correo
    subject = '[ResucitAR] Notificación a Responsables de la Sede'
    from_email = 'ResucitAR <%s>' % (settings.EMAIL_HOST_USER)
    reply_to_email = 'noreply@resucitar.com'

    # Plantilla para el contenido del correo
    text_content = get_template('mail/notificacion_responsables.txt')
    html_content = get_template('mail/notificacion_responsables.html')

    # Obtener la ubicación del usuario desde la URL
    user_lat = request.GET.get('user_lat', '')
    user_lng = request.GET.get('user_lng', '')

    # Iterar sobre los responsables y enviar un correo a cada uno
    for responsable in responsables:
        to_email = responsable.email

        context = {
            'responsable': responsable,
            'solicitante': request.user,
            'sede': sede,
            'user_lat': user_lat,
            'user_lng': user_lng,
        }

        text_content_rendered = text_content.render(context)
        html_content_rendered = html_content.render(context)

        # Crear el objeto de correo electrónico
        email = EmailMultiAlternatives(subject, text_content_rendered, from_email, to=[to_email,], reply_to=[reply_to_email,])
        email.mixed_subtype = 'related'
        email.content_subtype = 'html'
        email.attach_alternative(html_content_rendered, 'text/html')

        # Enviar el correo
        email.send(fail_silently=False)

    return redirect('Dash')



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

    if request.method == 'POST':
        form = SolicitudAprobacionForm(request.POST)
        if form.is_valid():
            representante = request.user.representante
            sede_id = form.cleaned_data['entidad_sede']  # Obtener el ID de la sede
            sede = Sede.objects.get(id=sede_id)  # Obtener la instancia de la sede
            motivo = form.cleaned_data['motivo']

            try:
                espacio_obligado = EspacioObligado.objects.get(sede=sede)
            except EspacioObligado.DoesNotExist:
                mensaje = "El EspacioObligado asociado a esta sede no existe"
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'mensaje': mensaje})


            # Verificar que el representante no exista en la lista de representantes
            if sede.representantes.filter(representante_id=representante.representante_id).exists():
                mensaje = "Usted ya está asociado a esta sede"
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'mensaje':mensaje})
            
            # Verificar si ya existe una solicitud con la misma entidad y sede
            if SolicitudAprobacion.objects.filter(entidad=sede.entidad, sede=sede).exists():
                # Mostrar un mensaje de error
                mensaje = "Ud ya tiene una solicitud de aprobación para la entidad-sede"
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'mensaje':mensaje})
            
            
            solicitud_aprobacion = SolicitudAprobacion(
                representante=representante, 
                entidad=sede.entidad, 
                sede=sede, 
                motivo=motivo
            )
            solicitud_aprobacion.save() 
            return redirect('/dash')
    else:
        form = SolicitudAprobacionForm()

    return render(request, 'solicitud_aprobacion.html', {'form': form})



def lista_solicitudes_pendientes(request):   

    solicitudes_pendientes = SolicitudAprobacion.objects.filter(aprobado=False)
    return render(request, 'lista_solicitudes_pendientes.html', {'solicitudes_pendientes': solicitudes_pendientes})

def aprobar_solicitud(request, solicitud_id):
    if not request.user.is_authenticated or not request.user.adminprovincial:
        return HttpResponseForbidden("No tienes permisos para realizar esta acción.")
    
    solicitud = get_object_or_404(SolicitudAprobacion, pk=solicitud_id)

    representante_solicitud = solicitud.representante
    sede_solicitud = solicitud.sede
    sede_solicitud.representantes.add(representante_solicitud)
    sede_solicitud.save()

    solicitud.aprobado = True
    solicitud.save()
    return redirect('lista_solicitudes_pendientes')

def rechazar_solicitud(request, solicitud_id):
    if not request.user.is_authenticated or not request.user.adminprovincial:
        return HttpResponseForbidden("No tienes permisos para realizar esta acción.")
    
    solicitud = get_object_or_404(SolicitudAprobacion, pk=solicitud_id)
    solicitud.aprobado = False

    solicitud.save()
    return redirect('lista_solicitudes_pendientes')


def solicitud_aprobacion(request):

    if request.method == 'POST':
        form = SolicitudAprobacionForm(request.POST)
        if form.is_valid():
            representante = request.user.representante
            sede_id = form.cleaned_data['entidad_sede']  # Obtener el ID de la sede
            sede = Sede.objects.get(id=sede_id)  # Obtener la instancia de la sede
            motivo = form.cleaned_data['motivo']

            try:
                espacio_obligado = EspacioObligado.objects.get(sede=sede)
            except EspacioObligado.DoesNotExist:
                
                print("!!!!!!!!!El EspacioObligado asociado a esta sede no existe")
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'mensaje': mensaje})


            # Verificar que el representante no exista en la lista de representantes
            if sede.representantes.filter(representante_id=representante.representante_id).exists():
                mensaje = "Usted ya está asociado a esta sede"
                print("!!!!!!!!!!Usted ya está asociado a esta sede")
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'mensaje':mensaje})
            
            # Verificar si ya existe una solicitud con la misma entidad y sede
            if SolicitudAprobacion.objects.filter(entidad=sede.entidad, sede=sede).exists():
                # Mostrar un mensaje de error
                print("!!!!!!!Ud ya tiene una solicitud de aprobación para la entidad-sede")
                return render(request, 'solicitud_aprobacion.html', {'form': form, 'mensaje':mensaje})
            
            
            solicitud_aprobacion = SolicitudAprobacion(
                representante=representante, 
                entidad=sede.entidad, 
                sede=sede, 
                motivo=motivo
            )
            solicitud_aprobacion.save() 
            return redirect('/dash')
    else:
        form = SolicitudAprobacionForm()

    return render(request, 'solicitud_aprobacion.html', {'form': form})



def lista_solicitudes_pendientes(request):   

    solicitudes_pendientes = SolicitudAprobacion.objects.filter(aprobado=False)
    return render(request, 'lista_solicitudes_pendientes.html', {'solicitudes_pendientes': solicitudes_pendientes})

# MODULO CERTIFICANTE
def listar_espacios_obligados_certificante(request):
    certificante = Certificante.objects.get(user=request.user)
    certificante_provincias = certificante.provincias.all()

    espacios_obligados = []
    for provincia in certificante_provincias:
        espacios = EspacioObligado.objects.filter(sede__provincia=provincia)
        # Agrega los espacios obligados a la lista
        espacios_obligados.extend(espacios)

    return render(request, 'certificante/listar_espacios_obligados.html', {'espacios_obligados': espacios_obligados})

# VISITA USUARIO CERTIFICANTE
def nueva_visita(request, espacio_obligado_id):
    if request.method == "POST":
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            espacio_obligado = EspacioObligado.objects.get(id=espacio_obligado_id)
            visita.espacio_obligado_id = espacio_obligado
            certificante = Certificante.objects.get(user=request.user)
            visita.certificante_id = certificante
            visita.save()
            if visita.resultado == 'aprobado':
                espacio_obligado.estado = 'CARDIO ASISTIDO CERTIFICADO'
                espacio_obligado.save()
            else:
                espacio_obligado.estado = 'CARDIO ASISTIDO'
                espacio_obligado.save()
            messages.success(request, 'Visita registrada correctamente.')
            return redirect('listar_espacios_obligados_certificante')
    else:
        form = VisitaForm()
    espacio_obligado = EspacioObligado.objects.get(id=espacio_obligado_id)
    
    return render(request, 'certificante/nueva_visita.html', {'form': form, 'espacio_obligado': espacio_obligado})

def listar_visitas(request, espacio_obligado_id):
    visitas = Visita.objects.filter(espacio_obligado_id=espacio_obligado_id).order_by('-fecha_hora')
    return render(request, 'certificante/listar_visitas.html', {'visitas': visitas})


def eliminar_visita(request, visita_id):
    visita = Visita.objects.get(id=visita_id)
    if request.method == 'POST':
        espacio_obligado = EspacioObligado.objects.get(id=visita.espacio_obligado_id.id)
        espacio_obligado.estado = 'CARDIO ASISTIDO'
        espacio_obligado.save()
        visita.delete()
    messages.success(request, 'Visita eliminada correctamente.')
    return redirect('listar_visitas', espacio_obligado_id=visita.espacio_obligado_id.id)
    


# Muerte Súbita
def registrar_muerte_subita(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    if request.method == 'POST':
        form = EventoMuerteSubitaForm(sede, request.POST)
        if form.is_valid():
            muerte_subita = form.save(commit=False)
            muerte_subita.sede_id = sede
            muerte_subita.representante_id = request.user.representante
            muerte_subita.save()
            return redirect('listar_mis_entidades_sedes')
    else:
        form = EventoMuerteSubitaForm(sede)
    return render(request, 'sede/registrar_muerte_subita.html', {'form': form, 'sede': sede})


def listar_eventos_muerte_subita(request, sede_id):
    sede = Sede.objects.get(id=sede_id)
    eventos = EventoMuerteSubita.objects.filter(sede_id=sede_id)
    return render(request, 'sede/listar_eventos_muerte_subita.html', {'eventos': eventos, 'sede': sede})
