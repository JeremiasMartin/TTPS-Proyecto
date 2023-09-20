from django import forms
from .models import  Usuario
import random
from django.utils.encoding import force_str
import string

class UserSign(forms.Form):
   email = forms.EmailField(max_length=200, required=True)
   password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())


class UsuarioRegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

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
        self.fields['email'] = forms.EmailField(required=True)
        self.fields['telefono'].label = force_str("Teléfono")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso. Prueba con otro')
        return email
    
    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
            email=self.cleaned_data['email'],
            password=''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Genera una contraseña aleatoria de 8 caracteres
        )
        representante = super(RepresentanteForm, self).save(commit=False)
        representante.user = usuario
        if commit:
            representante.save()
        return representante
    

class EditarRepresentanteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.apellido = self.cleaned_data['apellido']
        user.telefono = self.cleaned_data['telefono']
        if commit:
            user.save()
        return user
