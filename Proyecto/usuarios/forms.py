from django import forms
from .models import Usuario
import random
from django.utils.encoding import force_str
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class UserSign(forms.Form):
    email = forms.EmailField(required=True, max_length=200, label=force_str(
        "Correo electrónico"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico', 'class': 'form-control', 'id': 'email'}))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Ingrese su contraseña', 'class': 'form-control', 'id': 'password'}, render_value=False))


class UsuarioRegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2


class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellido', 'telefono', 'email']

    def __init__(self, *args, **kwargs):
        super(RepresentanteForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(required=True, label=force_str(
            "Nombre"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class': 'form-control'}))

        self.fields['apellido'] = forms.CharField(required=True, label=force_str(
            "Apellido"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido', 'class': 'form-control'}))

        self.fields['email'] = forms.EmailField(required=True, label=force_str(
            "Correo electrónico"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico', 'class': 'form-control'}))

        self.fields['dni'] = forms.IntegerField(required=True, label=force_str(
            "DNI"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su DNI', 'class': 'form-control', 'type': 'number'}))

        self.fields['telefono'] = forms.IntegerField(required=True, label=force_str(
            "Teléfono"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su teléfono', 'class': 'form-control', 'type': 'number'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este correo electrónico ya está en uso. Prueba con otro')
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError(
                'Este DNI ya está en uso. Prueba con otro')
        return dni

    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
            email=self.cleaned_data['email'],
            # Genera una contraseña aleatoria de 8 caracteres
            password=''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
        )
        representante = super(RepresentanteForm, self).save(commit=False)
        representante.user = usuario
        if commit:
            representante.save()
        return representante


class EditarRepresentanteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono', 'dni']

    def __init__(self, *args, **kwargs):
        super(EditarRepresentanteForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(required=True, label=force_str(
            "Nombre"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class': 'form-control'}))

        self.fields['apellido'] = forms.CharField(required=True, label=force_str(
            "Apellido"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido', 'class': 'form-control'}))

        self.fields['dni'] = forms.IntegerField(required=True, label=force_str(
            "DNI"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su DNI', 'class': 'form-control', 'type': 'number'}))

        self.fields['telefono'] = forms.IntegerField(required=True, label=force_str(
            "Teléfono"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su teléfono', 'class': 'form-control', 'type': 'number'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.apellido = self.cleaned_data['apellido']
        user.telefono = self.cleaned_data['telefono']
        if commit:
            user.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Contraseña anterior"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",
                   "class": "form-control", "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}),
    )

    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}),
    )

    error_messages = {
        "password_incorrect": _(
            "Su antigua contraseña fue ingresada incorrectamente. Por favor ingréselo nuevamente.",
        ),
        "password_mismatch": _("Los dos campos de contraseña no coinciden."),
    }
    

class AdminProvincialForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellido', 'telefono', 'email']

    def __init__(self, *args, **kwargs):
        super(AdminProvincialForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(required=True, label=force_str(
            "Nombre"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class': 'form-control'}))

        self.fields['apellido'] = forms.CharField(required=True, label=force_str(
            "Apellido"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido', 'class': 'form-control'}))

        self.fields['email'] = forms.EmailField(required=True, label=force_str(
            "Correo electrónico"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico', 'class': 'form-control'}))

        self.fields['dni'] = forms.IntegerField(required=True, label=force_str(
            "DNI"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su DNI', 'class': 'form-control', 'type': 'number'}))

        self.fields['telefono'] = forms.IntegerField(required=True, label=force_str(
            "Teléfono"), widget=forms.TextInput(attrs={'placeholder': 'Ingrese su teléfono', 'class': 'form-control', 'type': 'number'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este correo electrónico ya está en uso. Prueba con otro')
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError(
                'Este DNI ya está en uso. Prueba con otro')
        return dni

    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
            email=self.cleaned_data['email'],
            # Genera una contraseña aleatoria de 8 caracteres
            password=''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
        )
        adminProvincial = super(AdminProvincialForm, self).save(commit=False)
        adminProvincial.user = usuario
        if commit:
            adminProvincial.save()
        return adminProvincial
