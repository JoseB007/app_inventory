from django.forms import *
from apps.productos.models import Producto


class FormularioProducto(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        # Agregar todos los campos en el formulario
        # fields = ['nombre', 'descripcion', 'precio', 'cantidad_en_stock', 'categoria']
        fields = '__all__' 
        labels = {
            'descripcion': 'Descripción',
            'categoria': 'Categoría'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del producto',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción para el producto',
                    'rows': 3,
                    'cols': 3,
                }
            )
        }
        exclude = ['cantidad_en_stock']
