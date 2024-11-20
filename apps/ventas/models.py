from django.db import models
from django.forms import model_to_dict
from django.utils.timezone import localtime

from apps.clientes.models import Cliente
from apps.productos.models import Producto
from apps.empleados.models import Empleado

# Create your models here.


class OrdenDeVenta(models.Model):
    PENDIENTE = 'Pendiente'
    CANCELADA = 'Cancelada'
    ANULADA = 'Anulada'

    ESTADO_DE_ORDEN = [
        (PENDIENTE, 'Pendiente'),
        (CANCELADA, 'Cancelada'),
        (ANULADA, 'Anulada'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(
        max_length=20, choices=ESTADO_DE_ORDEN, default=CANCELADA)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Orden de Venta No. {self.id}"

    def orden_Json(self):
        orden = model_to_dict(self, exclude=["empleado"])
        #orden['empleado'] = self.empleado.usuario.get_full_name()
        orden['cliente'] = self.cliente.nombre
        orden['fecha'] = localtime(self.fecha).strftime('%d de %b de %Y, a las %H:%M')
        return orden


class DetalleOrdenDeVenta(models.Model):
    orden_de_venta = models.ForeignKey(OrdenDeVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    
    def json_detalle_venta(self):
        detalle_venta = model_to_dict(self)
        detalle_venta['producto'] = self.producto.nombre
        return detalle_venta

    def __str__(self):
        return f"Detalle {self.id} de Orden de Venta {self.orden_de_venta.id}"
