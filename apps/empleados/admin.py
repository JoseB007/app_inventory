from django.contrib import admin
from .models import Empleado

# Register your models here.
class EmpleadoAdmin(admin.ModelAdmin):
    # Personalizar la plantilla para ingresar los datos
    fieldsets = [
        ('Datos personales', {
            'fields': ['usuario' ,'documento_de_identidad']
        }),
        ('Datos de contacto', {
            'fields': ['telefono', 'direccion'], 
            'classes': ['collapse']
        }),
    ]
    
    # Personalizar la plantilla para mostrar los datos
    list_display = ['id', 'usuario', 'documento_de_identidad', 'telefono', 'direccion', 'fecha_contratacion']

admin.site.register(Empleado, EmpleadoAdmin)