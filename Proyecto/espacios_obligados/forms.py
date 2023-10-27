from django import forms
from .models import Entidad, Sede, Provincias, DEA
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis.geos import Point
from django.contrib.gis import forms as gis_forms

class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = ['razon_social', 'cuit', 'sector', 'tipo']

class SedeForm(forms.ModelForm):

    ubicacion = gis_forms.PointField(widget=LeafletWidget())

    class Meta:
        model = Sede
        fields = ['nombre', 'cant_personas_externas', 'superficie', 'cant_personal', 'direccion', 'provincia', 'ubicacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].required = False
    
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion:
            raise forms.ValidationError('Debe seleccionar una ubicación en el mapa.')
        return ubicacion

    def save(self, commit=True):
        sede = super().save(commit=False)
        coordenadas = self.cleaned_data.get('ubicacion')
        if coordenadas:
            sede.ubicacion = coordenadas
        if commit:
            sede.save()
        return sede
    


class EditSedeForm(forms.ModelForm):

    ubicacion = gis_forms.PointField(widget=LeafletWidget())
    class Meta:
        model = Sede
        fields = ['nombre', 'cant_personas_externas', 'superficie', 'cant_personal', 'direccion', 'ubicacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].required = False

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion:
            raise forms.ValidationError('Debe seleccionar una ubicación en el mapa.')
        return ubicacion
    
    def save(self, commit=True):
        sede = super().save(commit=False)
        coordenadas = self.cleaned_data.get('ubicacion')
        if coordenadas:
            sede.ubicacion = coordenadas
        if commit:
            sede.save()
        return sede


class DeclaracionJuradaForm(forms.ModelForm):
    personal_capacitado = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    senaletica = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    protocolo_accion = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    sistema_emergencia = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    deas_decreto = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Sede
        fields = ['personal_capacitado', 'senaletica', 'protocolo_accion', 'sistema_emergencia', 'deas_decreto']


class DEAForm(forms.ModelForm):
    aprobacion_ANMAT = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    marca = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    modelo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero_serie = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_representativo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.ChoiceField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DEA
        fields = ['aprobacion_ANMAT', 'marca', 'modelo', 'numero_serie', 'nombre_representativo', 'estado']
