from django.contrib import admin
from .models import OrdenDeCompra, DetalleDeCompra

# Register your models here.
class DetalleDeCompraInline(admin.TabularInline):
    model = DetalleDeCompra
    extra = 2


class OrdenDeCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_de_orden', 'total', 'estado', 'proveedor']
    inlines = [DetalleDeCompraInline]

admin.site.register(OrdenDeCompra, OrdenDeCompraAdmin)


class DetalleDeCompraAdmin(admin.ModelAdmin):
    list_display = ['orden_de_compra', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

admin.site.register(DetalleDeCompra, DetalleDeCompraAdmin)