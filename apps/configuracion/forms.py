from django.forms import *

from apps.configuracion.models import Configuracion

class FormConfig(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_empresa'].initial = Configuracion.obtener_config()['nombre_empresa']
        self.fields['nit'].initial = Configuracion.obtener_config()['nit']
        self.fields['email'].initial = Configuracion.obtener_config()['email']
        self.fields['telefono'].initial = Configuracion.obtener_config()['telefono']

    class Meta:
        model = Configuracion
        fields = "__all__"
        widgets = {
            'nombre_empresa': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de su Organización'
                }
            ),
            'nit': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el NIT de su Organización'
                }
            ),
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el correo electrónico de su Organización'
                }
            ),
            'telefono': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el teléfono de su Organización'
                }
            ),
        }
