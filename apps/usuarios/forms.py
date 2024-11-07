from typing import Any

from django.forms import *

from apps.usuarios.models import Usuario


class FormularioUsuario(ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus', 'required': True})
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['required'] = True

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'groups']
        widgets = {
            'groups': SelectMultiple(attrs={
                'class': 'form-control'
            })
        }


class FormularioPerfilUsuario(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus', 'required': True})
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['required'] = True

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': PasswordInput(render_value=True)
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')
    #     email = cleaned_data.get('email')

    #     if first_name == "":
    #         self.add_error('first_name', 'El usuario debe tener un nombre.')

    #     if last_name == "":
    #         self.add_error('last_name', 'El usuario debe tener un apellido.')

    #     if email == "":
    #         self.add_error('email', 'El usuario debe tener una dirección de correo electrónico.')

    #     return cleaned_data
