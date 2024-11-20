import locale

from django.db import models
from django.forms import model_to_dict
from django.utils.timezone import localtime

from apps.proveedores.models import Proveedor
from apps.productos.models import Producto
from apps.empleados.models import Empleado

# Create your models here.
class OrdenDeCompra(models.Model):
    PENDIENTE = 'Pendiente'
    CANCELADA = 'Cancelada'
    ANULADA = 'Anulada'

    ESTADO_DE_ORDEN = [
        (PENDIENTE, 'Pendiente'),
        (CANCELADA, 'Cancelada'),
        (ANULADA, 'Anulada'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    # auto_now_add: Establece el campo con la fecha y hora actual cuando se crea el objeto por primera vez.
    fecha_de_orden = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_DE_ORDEN, default=CANCELADA)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Orden de Compra No. {self.id}"
    
    def orden_json(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        orden = model_to_dict(self, exclude=["empleado"])
        orden['estado'] = self.get_estado_display()
        orden['proveedor'] = self.proveedor.nombre if self.proveedor else None
        fecha_formateada = localtime(self.fecha_de_orden).strftime('%d de %B de %Y a las %H:%M')
        orden['fecha_de_orden'] = fecha_formateada
        
        return orden
    

class DetalleDeCompra(models.Model):
    orden_de_compra = models.ForeignKey(OrdenDeCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT) 
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def detalle_json(self):
        detalle = model_to_dict(self, exclude=['id', 'orden_de_compra'])
        detalle['producto'] = self.producto.nombre if self.producto else None
        return detalle

    def __str__(self):
        return f"Detalle {self.id} de Orden de Compra {self.orden_de_compra.id}"