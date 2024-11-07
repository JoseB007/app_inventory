from django.forms import *

from apps.proveedores.models import Proveedor


class FormularioProveedor(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['placeholder'] = f'Ingrese el {campo.label.lower()} del proveedor'
            campo.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True
        self.fields['direccion'].widget.attrs['placeholder'] = 'Ingrese una dirección para el proveedor'

    class Meta:
        model = Proveedor
        fields = '__all__'

        widgets = {
            'direccion': Textarea(attrs={
                'rows': 3,
                'cols': 3,
            })
        } 