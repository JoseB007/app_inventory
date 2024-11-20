from django.db import models
from django.forms import model_to_dict
from django.utils.timezone import localtime, now


from apps.compras.models import OrdenDeCompra
from apps.ventas.models import OrdenDeVenta
from apps.empleados.models import Empleado


class MovimientoInventario(models.Model):
    fecha = models.DateField(default=now, unique=True)  # Día del movimiento
    total_ventas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_compras = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    ordenes_venta = models.ManyToManyField(OrdenDeVenta, blank=True)
    ordenes_compra = models.ManyToManyField(OrdenDeCompra, blank=True)
    
    def actualizar_totales(self):
        """Recalcula los totales de ventas y compras."""
        self.total_ventas = sum(orden.total for orden in self.ordenes_venta.all())
        self.total_compras = sum(orden.total for orden in self.ordenes_compra.all())
        self.save()
    
    def __str__(self):
        return f"Movimiento del {self.fecha}: Ventas ${self.total_ventas}, Compras ${self.total_compras}"
    
    def json_mov_inventario(self):
        inventario = model_to_dict(self, exclude=["ordenes_venta", "ordenes_compra"])
        inventario['fecha'] = self.fecha.strftime('%d de %b de %Y')
        return inventario


