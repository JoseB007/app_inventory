from django.db import models
from django.forms import model_to_dict
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

# Create your models here.
class Usuario(AbstractUser):
      
    def json_usuario(self):
        usuario = model_to_dict(self, exclude=['password', 'is_staff', 'user_permissions', 'is_active'])
        usuario['date_joined'] = localtime(self.date_joined).strftime('%d-%b-%Y')
        usuario['last_login'] = localtime(self.last_login).strftime('%d %b %Y, a las %H:%M') if self.last_login else None
        usuario['is_superuser'] = 'Superusuario' if self.is_superuser else 'Usuario'
        usuario['groups'] = list(self.groups.values_list('name', flat=True))
        return usuario
    
    def save(self, *args, **kwargs):
        if self.pk is None and not self.is_superuser:
            self.clean()

        if self.pk:
            user = Usuario.objects.get(pk=self.pk)
            if user.password != self.password:
                self.set_password(self.password)
        
        if not self.pk:
            self.set_password(self.password)

        super().save(*args, **kwargs)


    def clean(self):
        # Solo valida si el usuario no es superusuario
        if not self.is_superuser:
            if not self.first_name:
                raise ValidationError({'first_name': 'El usuario debe tener un nombre.'})
            
            if not self.last_name:
                raise ValidationError({'last_name': 'El usuario debe tener un apellido.'})
            
            if not self.email:
                raise ValidationError({'email': 'El usuario debe tener una dirección de correo electrónico.'})
