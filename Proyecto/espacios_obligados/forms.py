from django import forms
from .models import Entidad, Sede, Provincias, DEA, HistorialDEA, Responsable
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
    numero_serie = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_representativo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    solidario = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

        
    class Meta:
        model = DEA
        fields = ['marca', 'modelo', 'numero_serie', 'nombre_representativo', 'solidario']


class DEAEditForm(forms.ModelForm):
    numero_serie = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_representativo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    solidario = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = DEA
        fields = ['numero_serie', 'nombre_representativo', 'solidario']


class DEAServicioForm(forms.ModelForm):
    dia = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    opciones = [
        ('Reparación', 'Reparación'),
        ('Mantenimiento', 'Mantenimiento'),
    ]
    servicio = forms.ChoiceField(required=True, choices=opciones, widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = HistorialDEA
        fields = ['dia', 'servicio', 'observaciones']



class ResponsableForm(forms.ModelForm):
    nombre = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Responsable
        fields = ['nombre', 'apellido', 'telefono', 'email']