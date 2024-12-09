from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Configuracion(models.Model):
    nombre_empresa = models.CharField(
        max_length=150,
        help_text="Establecer el nombre de su empresa",
        verbose_name="Nombre de la empresa"
    )
    nit = models.CharField(
        max_length=10,
        verbose_name="NIT"
    )
    email = models.EmailField(
        verbose_name="Correo electrónico"
    )
    telefono = models.CharField(
        max_length=10,
        verbose_name="Télefono"
    )

    def obtener_config():
        config = Configuracion.objects.first()
        datos = {}
        if config:
            datos['nombre_empresa'] = config.nombre_empresa
            datos['nit'] = config.nit
            datos['email'] = config.email
            datos['telefono'] = config.telefono
        else:
            datos['nombre_empresa'] = "Mi Empresa"
            datos['nit'] = "0000000000"
            datos['email'] = "mi_empresa@example.com"
            datos['telefono'] = "1234567890"
        return datos
    
    def clean(self):
        super().clean()
        if not self.nit.isdigit():
            raise ValidationError({'nit': 'El NIT solo debe contener números.'})
        
        if not self.telefono.isdigit():
            raise ValidationError({'telefono': 'El teléfono solo debe contener números'})

