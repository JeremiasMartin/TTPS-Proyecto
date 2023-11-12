from django import forms
from .models import Entidad, Sede, Provincias, DEA, HistorialDEA, Responsable, Visita, SolicitudAprobacion,EspacioObligado, EventoMuerteSubita
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


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['fecha_hora', 'observaciones', 'resultado']
    
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'data-inputmask-alias': 'datetime', 'data-inputmask-inputformat': 'yyyy-mm-dd HH:MM', 'data-mask': 'data-mask', 'autofocus': 'autofocus'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resultado': forms.Select(attrs={'class': 'form-control'}, choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]),
        }

class SolicitudAprobacionForm(forms.ModelForm):
    entidad_sede = forms.ChoiceField(choices=(), required=True)

    class Meta:
        model = SolicitudAprobacion
        fields = ['entidad_sede', 'motivo']

    def __init__(self, *args, **kwargs):
        super(SolicitudAprobacionForm, self).__init__(*args, **kwargs)

        opciones_entidad_sede = []

        for espacio_obligado in EspacioObligado.objects.all():
            sede = espacio_obligado.sede
            opciones_entidad_sede.append((f'{sede.id}', f'{sede.entidad.razon_social} - {sede.nombre}'))

        self.fields['entidad_sede'].choices = opciones_entidad_sede

    def clean_entidad_sede(self):
        sede_id = self.cleaned_data['entidad_sede']
        return sede_id  
    
    

class EventoMuerteSubitaForm(forms.ModelForm):
    def __init__(self, sede, *args, **kwargs):
        super(EventoMuerteSubitaForm, self).__init__(*args, **kwargs)
        self.fields['dea'].queryset = DEA.objects.filter(sede=sede)

    class Meta:
        model = EventoMuerteSubita
        fields = ['fecha', 'sexo', 'edad', 'fallecido', 'rcp', 'tiempo_rcp', 'dea', 'inconveniente', 'descarga_electrica', 'cantidad_descarga', 'observaciones']

        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}, choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')]),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'fallecido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rcp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_rcp': forms.NumberInput(attrs={'class': 'form-control'}),
            'inconveniente': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descarga_electrica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cantidad_descarga': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        def clean_rcp(self):
            rcp = self.cleaned_data['rcp']
            if rcp:
                tiempo_rcp = self.cleaned_data['tiempo_rcp']
                if not tiempo_rcp:
                    raise forms.ValidationError('Debe ingresar el tiempo de RCP.')
            return rcp
        
        def clean_descarga_electrica(self):
            descarga_electrica = self.cleaned_data['descarga_electrica']
            if descarga_electrica:
                cantidad_descarga = self.cleaned_data['cantidad_descarga']
                if not cantidad_descarga:
                    raise forms.ValidationError('Debe ingresar la cantidad de descargas.')
            return descarga_electrica
        