from django.shortcuts import render, redirect , get_object_or_404
from .forms import AdminProvincialForm, RepresentanteForm, UsuarioComunForm, CustomPasswordChangeForm, CertificanteForm
from .models import Provincias, Usuario, Representante ,AdminProvincial, UsuarioComun, Certificante, Provincias
from espacios_obligados.models import Sede,EspacioObligado 
import random
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib import messages
from .forms import UserSign, EditarRepresentanteForm
from django.template.loader import get_template
from Proyecto import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.urls import reverse_lazy
from datetime import date


def representante_signup(request):
    if request.method == 'POST':
        form = RepresentanteForm(request.POST)
        if form.is_valid():
            passwd = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyz0123456789', k=8))
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            dni = form.cleaned_data['dni']
            telefono = form.cleaned_data['telefono']

            usuario = Usuario.objects.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                password=passwd
            )

            representante = Representante.objects.create(
                user=usuario,
            )
            # FIXME: Comento envio de emails al registrarse
            subject = '[ResucitAR] Registro de Usuario Exitoso'
            from_email = 'ResucitAR <%s>' % (settings.EMAIL_HOST_USER)
            to_email = '%s' % (form.cleaned_data.get('email'))
            reply_to_email = 'noreply@resucitar.com'

            context = {
                'nombre': form.cleaned_data.get('nombre'),
                'password': passwd
            }
            text_content = get_template('usuario/mail_bienvenida.txt')
            html_content = get_template('usuario/mail_bienvenida.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[
                                           to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')
            email.send(fail_silently=False)
            messages.success(
                request, 'Registro exitoso. Verifique su correo electronico para obtener su contraseña.')

            return redirect('login')
    else:
        form = RepresentanteForm()
    return render(request, 'representante/form_representante.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserSign(data=request.POST)
        if form.is_valid():
            mail = form.cleaned_data.get("email")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(request, email=mail, password=contraseña)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('Dash')
            else:
                messages.error(
                    request, "Correo y/o contraseña incorrectos. Por favor! vuelva a ingresarlos", "danger")
        else:
            messages.error(request, "informacion")
    form = UserSign()
    context = {'form': form}
    return render(request, 'usuario/login.html', context)


def user_logout(request):

    django_logout(request)
    return redirect('/')


def perfil_representante(request):
    representante = Representante.objects.get(user=request.user)
    return render(request, 'representante/perfil_representante.html', {'representante': representante})


@login_required
def editar_perfil_representante(request):
    perfil = request.user
    if request.method == 'POST':
        form = EditarRepresentanteForm(
            request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
            messages.success(
                request, "¡Información actualizada correctamente!")
            return redirect('/usuarios/perfil_representante')
    else:
        form = EditarRepresentanteForm(instance=perfil)
    context = {'form': form, 'errors': form.errors}
    return render(request, 'representante/editar_perfil_representante.html', context)


class cambiar_contrasenia(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = "/usuarios/perfil_representante"


class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('/usuarios/login/')


login_after_password_change = login_required(
    LoginAfterPasswordChangeView.as_view())


def restablecer_contraseña(request):
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            mail = form.cleaned_data.get("email")
            if Usuario.objects.filter(email=mail).exists():
                form.save(from_email='proyecto@proyecto.com',
                          email_template_name='registration/password_reset_email.html', request=request)
                return redirect('/usuarios/restablecer_contrasenia_enviado')
            else:
                messages.error(
                    request, "El mail ingresado no se encuentra registrado en el sistema")
        else:
            messages.error(request, "No existe ese mail")
    form = PasswordResetForm()
    context = {'form': form}
    return render(request, 'usuario/cambio_de_clave/restablecer_contrasenia.html', context)


class restPasswordConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm


def restDone(request):

    return render(request, 'usuario/cambio_de_clave/restablecer_contrasenia_enviado.html')


def adminProvincial_signup(request):
    if request.method == 'POST':
        form = RepresentanteForm(request.POST)
        if form.is_valid():
            passwd = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyz0123456789', k=8))
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            dni = form.cleaned_data['dni']
            telefono = form.cleaned_data['telefono']

            usuario = Usuario.objects.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                password=passwd
            )

            adminProvincial = AdminProvincial.objects.create(
                user=usuario,
            )
            # FIXME: Comento envio de emails al registrarse
            subject = '[ResucitAR] Registro de Usuario Exitoso'
            from_email = 'ResucitAR <%s>' % (settings.EMAIL_HOST_USER)
            to_email = '%s' % (form.cleaned_data.get('email'))
            reply_to_email = 'noreply@resucitar.com'

            context = {
                'nombre': form.cleaned_data.get('nombre'),
                'password': passwd
            }
            text_content = get_template('usuario/mail_bienvenida.txt')
            html_content = get_template('usuario/mail_bienvenida.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[
                                           to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')
            email.send(fail_silently=False)
            messages.success(
                request, 'Registro exitoso. Verifique su correo electronico para obtener su contraseña.')

            return redirect('login')
    else:
        form = AdminProvincialForm()
    return render(request, 'adminProvincial/formAdminProvincial.html', {'form': form})


def inicioAdminProvincial(request):

    administrador = AdminProvincial.objects.get(user=request.user)
    provincias_asociadas = administrador.provincias.all()
    sedes_sin_espacio = Sede.objects.filter(espacioobligado__isnull=True).intersection(
        Sede.objects.filter(provincia__in=provincias_asociadas))
    return render(request, 'adminProvincial/inicioAdminProvincial.html', {'admin': administrador, 'provincias': provincias_asociadas, 'espacios': sedes_sin_espacio})


def cambiar_estado_espacio(request,sede_id):
    if request.method == 'POST':
        sede = Sede.objects.get(id=sede_id)
        espacio = EspacioObligado()
        espacio.sede = Sede.objects.get(id=sede_id)
        if request.POST.get('action') == 'aprobar':
            espacio.estado= 'EN PROCESO'

        elif request.POST.get('action') == 'rechazar':
            espacio.estado = 'RECHAZADO'
            espacio.motivo = request.POST.get('reason')
        espacio.fecha_creacion = date.today()
        print(espacio)
        espacio.save()

    return redirect('inicioAdminProvincial')

def cambiar_dias_validez(request):
    administrador = AdminProvincial.objects.get(user=request.user)
    provincias_asociadas = administrador.provincias.all()
       
    return render(request, 'adminProvincial/cambiar_dias_validez.html',{'admin':administrador,'provincias':provincias_asociadas})

def modificar_validez(request, provincia_id):
    if request.method == 'POST':
        nuevo_validez = request.POST.get('nuevo_validez')
        provincia = Provincias.objects.get(provincia_id=provincia_id)
        provincia.validez_certificado = nuevo_validez
        provincia.save()
        return redirect('cambiar_dias_validez')

  
def usuario_comun_signup(request):
    if request.method == 'POST':
        form = UsuarioComunForm(request.POST)
        if form.is_valid():
            passwd = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyz0123456789', k=8))
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            dni = form.cleaned_data['dni']
            telefono = form.cleaned_data['telefono']

            usuario = Usuario.objects.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                password=passwd
            )

            usuarioComun = UsuarioComun.objects.create(
                user=usuario,
            )

            subject = '[ResucitAR] Registro de Usuario Exitoso'
            from_email = 'ResucitAR <%s>' % (settings.EMAIL_HOST_USER)
            to_email = '%s' % (form.cleaned_data.get('email'))
            reply_to_email = 'noreply@resucitar.com'

            context = {
                'nombre': form.cleaned_data.get('nombre'),
                'password': passwd
            }
            text_content = get_template('usuario/mail_bienvenida.txt')
            html_content = get_template('usuario/mail_bienvenida.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[
                                           to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')
            email.send(fail_silently=False)
            messages.success(
                request, 'Registro exitoso. Verifique su correo electronico para obtener su contraseña.')

            return redirect('login')
    else:
        form = UsuarioComunForm()
    return render(request, 'representante/form_representante.html', {'form': form})
  

def certificante_signup(request):
    if request.method == 'POST':
        form = CertificanteForm(request.POST)
        if form.is_valid():
            passwd = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyz0123456789', k=8))
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            dni = form.cleaned_data['dni']
            telefono = form.cleaned_data['telefono']

            usuario = Usuario.objects.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                password=passwd
            )

            # Creo el certificante y le agrego las provincias seleccionadas
            certificante = Certificante.objects.create(
                user=usuario,
            )
            provincias_seleccionadas = form.cleaned_data['provincias']
            provincias_ids = [
                provincia.pk for provincia in provincias_seleccionadas]

            certificante.agregar_provincias(provincias_ids)

            subject = '[ResucitAR] Registro de Usuario Exitoso'
            from_email = 'ResucitAR <%s>' % (settings.EMAIL_HOST_USER)
            to_email = '%s' % (form.cleaned_data.get('email'))
            reply_to_email = 'noreply@resucitar.com'

            context = {
                'nombre': form.cleaned_data.get('nombre'),
                'password': passwd
            }
            text_content = get_template('usuario/mail_bienvenida.txt')
            html_content = get_template('usuario/mail_bienvenida.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[
                                           to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')
            email.send(fail_silently=False)
            messages.success(
                request, 'Registro exitoso. Verifique su correo electronico para obtener su contraseña.')

            return redirect('login')
    else:
        form = CertificanteForm()
        provincias = Provincias.objects.all()
    return render(request, 'certificante/formCertificante.html', {'form': form, 'provincias': provincias})