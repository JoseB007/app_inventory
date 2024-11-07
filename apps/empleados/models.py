from django.db import models
from django.forms import model_to_dict

from apps.usuarios.models import Usuario

# Create your models here.
class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    documento_de_identidad = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=10)
    direccion = models.TextField(blank=True, null=True)
    fecha_contratacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Contratación')

    def __str__(self):
        return f'{self.usuario.get_full_name()} - ({self.usuario.username})' if self.usuario.first_name else self.usuario.username

    def empleado_to_json(self):
        empleado = model_to_dict(self)
        empleado['fecha_contratacion'] = self.fecha_contratacion.strftime('%d-%b-%Y')
        empleado['usuario'] = self.usuario.get_full_name() if self.usuario.first_name else None
        empleado['correo_electronico'] = self.usuario.email if self.usuario.email else None
        
        return empleado
        

    