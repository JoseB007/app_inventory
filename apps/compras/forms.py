from django.forms import *

# from apps.productos.models import Categoria, Producto
from apps.compras.models import OrdenDeCompra, DetalleDeCompra
from apps.proveedores.models import Proveedor


class FormularioOrdenDeCompra(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['autocomplete'] = 'off'
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
    
    class Meta:
        model = OrdenDeCompra
        fields = '__all__'
        widgets = {
            'subtotal': TextInput,
            'iva': TextInput,
            'total': TextInput,
        }


class FormularioFiltros(Form):
    proveedor = ModelChoiceField(
        Proveedor.objects.all(),
        label="Proveedor",
        widget=Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    month_ini = DateField(
        required=False,
        widget=DateInput(
            attrs={
                'type': 'date',  # Hace que el navegador muestre un selector de fecha
                'class': 'form-control',  # Agrega clases CSS para Bootstrap
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
            choices=OrdenDeCompra.ESTADO_DE_ORDEN,
            attrs={
                'class': 'form-check-input'
            }
        ),
        initial=OrdenDeCompra.ESTADO_DE_ORDEN[1]
    )

# class FormularioProducto(Form):
#     productos = ModelChoiceField(label="", queryset=Producto.objects.all(), widget=Select(attrs={
#         'class': 'form-control'
#     }))


# class FormularioAutoCompleteProducto(Form):
#     productos = CharField(label='Buscar producto:', max_length=150, widget=TextInput(attrs={
#         'class': 'form-control',
#         'autocomplete': 'off',
#         'id': 'id_autocomplete',
#     }))
