from django.forms import *

from apps.ventas.models import OrdenDeVenta


class FormularioOrdenDeVenta(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'

        self.fields['iva'].widget.attrs['readonly'] = True
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True

        # Configurar el campo 'cliente' para que seleccione la primera opción a través de '.queryset.exists()'
        if self.fields['cliente'].queryset.exists():
            self.fields['cliente'].initial = self.fields['cliente'].queryset.first().pk

    class Meta:
        model = OrdenDeVenta
        fields = '__all__'
        
        widgets = {
            'iva': TextInput(),
            'subtotal': TextInput(),
            'total': TextInput(),
        }
        
