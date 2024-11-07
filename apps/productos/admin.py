from django.contrib import admin
from .models import Categoria, Producto

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Categoria, CategoriaAdmin)


class ProductoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Datos principales', {
            'fields': ['nombre', 'descripcion', 'categoria', 'precio']
        }),
        ('Inventario', {
            'fields': ['cantidad_en_stock']
        }),
    ]
    
    list_display = ['nombre', 'descripcion', 'categoria', 'precio', 'cantidad_en_stock']

admin.site.register(Producto, ProductoAdmin)
