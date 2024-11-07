from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    documento_identidad = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    correo_electronico = models.EmailField(unique=True, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def jsonCliente(self):
        cliente = model_to_dict(self)
        return cliente
    

