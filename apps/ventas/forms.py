from django.forms import *

from apps.ventas.models import OrdenDeVenta
from apps.clientes.models import Cliente


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


class FormularioFiltros(Form):
    cliente = ModelChoiceField(
        Cliente.objects.all(), 
        label="Cliente", 
        widget=Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    # MESES = {
    #     None: "---------",
    #     "1": "Enero",
    #     "2": "Febrero",
    #     "3": "Marzo",
    #     "4": "Abril",
    #     "5": "Mayo",
    #     "6": "Junio",
    #     "7": "Julio",
    #     "8": "Agosto",
    #     "9": "Septiembre",
    #     "10": "Octubre",
    #     "11": "Noviembre",
    #     "12": "Diciembre",

    # }
    # mes_venta = ChoiceField(choices=MESES, required=False)
    # mes_venta.widget.attrs.update({'class': 'form-control'})

    month_ini = DateField(
        required=False,
        widget=DateInput(
            attrs={
                'type': 'date',  # Hace que el navegador muestre un selector de fecha
                'class': 'form-control',  # Agrega clases CSS para Bootstrap
                'placeholder': 'Seleccione una fecha',
            }
        ),
    )
    
    month_end = DateField(
        required=False,
        widget=DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
    )

    estate = NullBooleanField(
        widget=RadioSelect(
            choices=OrdenDeVenta.ESTADO_DE_ORDEN,
            attrs={
                'class': 'form-check-input'
            }
        ),
        initial=OrdenDeVenta.ESTADO_DE_ORDEN[1]
    )
    
    # def clean(self):
    #     cleaned_data = super().clean()

    #     client = cleaned_data.get('cliente')

    #     if not client:
    #         self.add_error('cliente', 'El campo "Cliente" es obligatorio')
     

    