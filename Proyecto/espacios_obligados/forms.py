from django import forms
from .models import Entidad, Sede, Provincias
from leaflet.forms.widgets import LeafletWidget

class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = ['razon_social', 'cuit', 'sector', 'tipo']

class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = ['nombre', 'cant_personas_externas', 'superficie', 'ubicacion', 'cant_personal', 'direccion', 'provincia']
        widgets = {
            'ubicacion': LeafletWidget(),
        }
        provincia = forms.ModelChoiceField(queryset=Provincias.objects.all())

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