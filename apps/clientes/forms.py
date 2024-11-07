from django.forms import *


from apps.clientes.models import Cliente


class FormularioCliente(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['autocomplete'] = 'off'

        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'telefono': 'Teléfono',
            'correo_electronico': 'Correo electrónico',
            'direccion': 'Dirección',
        }
        widgets = {
            'nombre': TextInput(attrs={
                'placeholder': 'Digite el nombre del cliente',
            }),
            'documento_identidad': TextInput(attrs={
                'placeholder': 'Digite el documento de identidad del cliente',
            }),
            'telefono': TextInput(attrs={
                'placeholder': 'Digite el teléfono del cliente',
            }),
            'correo_electronico': TextInput(attrs={
                'placeholder': 'Digite el correo electrónico del cliente',
            }),
            'direccion': TextInput(attrs={
                'placeholder': 'Digite la dirección del cliente',
            }),
        }
