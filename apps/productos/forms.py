from django.forms import *
from apps.productos.models import Producto, Categoria


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


# class FormFiltroCategoria(Form):
#     categoria = ModelChoiceField(
#         label="Categoría", queryset=Categoria.objects.all(), required=False)
#     #categoria.widget.attrs.update({'class': 'form-control'})


# class FormRangoPrecio(Form):
#     pracio_min = DecimalField(label="Precio mínimo",
#                               max_digits=10, decimal_places=2, required=False)
#     pracio_max = DecimalField(label="Precio máximo",
#                               max_digits=10, decimal_places=2, required=False)
#     # pracio_min.widget.attrs.update({'class': 'form-control'})
#     # pracio_max.widget.attrs.update({'class': 'form-control'})
    
