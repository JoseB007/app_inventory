from django.db import models
from django.forms import model_to_dict
from django.core.exceptions import ValidationError

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    direccion = models.TextField(verbose_name='Dirección')
    telefono = models.CharField(max_length=10, verbose_name='Teléfono')
    correo_electronico = models.EmailField(unique=True, verbose_name='Correo Electrónico')

    def __str__(self):
        return self.nombre
    
    def json_Proveedor(self):
        proveedor = model_to_dict(self)
        return proveedor
    
    def clean(self):
        if not self.telefono.isdigit():
            raise ValidationError({'telefono': 'El número de teléfono solo puede contener dígitos.'})