from django.db import models
from django.urls import reverse
from django.forms import model_to_dict

from simple_history.models import HistoricalRecords

# Create your models here.
class Categoria(models.Model):
    ALIMENTOS = 'alimentos'
    BELLEZA = 'belleza'
    DEPORTES = 'deportes'
    ELECTRODOMESTICOS = 'electrodomesticos'
    HIGIENE_SALUD = 'higiene_y_salud'
    MAQUILLAJE = 'maquillaje'
    VESTUARIO = 'vestuario'
    TECNOLOGIA = 'tecnologia'
    JUGUETERIA = 'jugueteria'
    PAPELERIA = 'papeleria'
    MUSICA_CINE = 'musica_y_cine'


    CATEGORIAS_DE_PRODUCTO = [
        (ALIMENTOS, 'Alimentos'),
        (BELLEZA, 'Belleza'),
        (DEPORTES, 'Deportes'),
        (ELECTRODOMESTICOS, 'Electrodomésticos'),
        (HIGIENE_SALUD, 'Higiene y Salud'),
        (MAQUILLAJE, 'Maquillaje'),
        (VESTUARIO, 'Vestuario'),
        (TECNOLOGIA, 'Tecnología'),
        (JUGUETERIA, 'Juguetería'),
        (PAPELERIA, 'Papelería'),
        (MUSICA_CINE, 'Música y Cine')
    ]

    tipo_categoria = models.CharField(max_length=20, choices=CATEGORIAS_DE_PRODUCTO, unique=True)

    def __str__(self):
        return self.tipo_categoria


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cantidad_en_stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    historial = HistoricalRecords()

    def json_producto(self):
        # producto = {
        #     'id': self.id, 
        #     'nombre': self.nombre, 
        #     'descripcion': self.descripcion, 
        #     'precio': str(self.precio), 
        #     'stock': self.cantidad_en_stock, 
        #     'categoria': self.categoria.tipo_categoria
        # }
        producto = model_to_dict(self, exclude=['historial'])
        producto['categoria'] = self.categoria.get_tipo_categoria_display()
        return producto
        
    def detalle_producto(self):
        return reverse('productos:detalle-producto', args=[self.pk])

    def __str__(self):
        return self.nombre
