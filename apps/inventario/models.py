from django.db import models
from apps.productos.models import Producto
from apps.empleados.models import Empleado
from apps.compras.models import OrdenDeCompra
from apps.ventas.models import OrdenDeVenta

# Create your models here.
class MovimientoInventario(models.Model):
    ENTRADA = 'Entrada'
    SALIDA = 'Salida'
    
    TIPO_MOVIMIENTO = [
        (ENTRADA, 'Entrada'),
        (SALIDA, 'Salida'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    orden_de_compra = models.ForeignKey(OrdenDeCompra, on_delete=models.SET_NULL, null=True, blank=True)
    orden_de_venta = models.ForeignKey(OrdenDeVenta, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Movimiento {self.id}. Tipo: {self.tipo} Producto: {self.producto.nombre}"
    