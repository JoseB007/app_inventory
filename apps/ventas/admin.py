from django.contrib import admin
from .models import OrdenDeVenta, DetalleOrdenDeVenta

# Register your models here.
class OrdenDeVentaAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrdenDeVenta, OrdenDeVentaAdmin)


class DetalleOrdenDeVentaAdmin(admin.ModelAdmin):
    pass

admin.site.register(DetalleOrdenDeVenta, DetalleOrdenDeVentaAdmin)
