from django.contrib import admin
from .models import Proveedor

# Register your models here.
class ProveedorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields':['nombre', 'direccion', 'telefono', 'correo_electronico']
        }),
    ]
    
    list_display = ['nombre', 'direccion', 'telefono', 'correo_electronico']

admin.site.register(Proveedor, ProveedorAdmin)
