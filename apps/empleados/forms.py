from django.forms import * # Importar la clase ModelForm

from .models import Empleado # Importar el modelo para los campos del formulario
from apps.usuarios.models import Usuario


class FormularioEmpleado(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['autocomplete'] = 'off'
            campo.field.widget.attrs['placeholder'] = f'Ingrese el {(campo.label).lower()} del empleado'

        self.fields['usuario'].label_from_instance = lambda obj: obj.get_full_name() if obj.first_name else obj.username
        
        if self.instance and self.instance.pk:
            self.fields['usuario'].initial = self.instance.usuario
            self.fields['usuario'].disabled = True
        else:
            self.fields['usuario'].queryset = Usuario.objects.exclude(pk__in=Empleado.objects.values_list('usuario'))
        

    def clean(self):
        cleaned_data = super().clean()
        telefono = cleaned_data.get('telefono')
        documento_de_identidad = cleaned_data.get('documento_de_identidad')

        if not telefono.isdigit():
            self.add_error('telefono', 'El teléfono debe contener solo números')

        if not documento_de_identidad.isdigit():
            self.add_error('documento_de_identidad', 'El documento de identidad debe contener solo números')

        return cleaned_data

    class Meta:
        model = Empleado
        fields = '__all__'
        labels = {
            'telefono': 'Teléfono',
            'documento_de_identidad': 'Documento de Identidad',
            'direccion': 'Dirección'
        }
        widgets = {
            'direccion': Textarea(
                attrs= {
                    'rows': 3,
                    'cols': 3,
                }
            )
        }




