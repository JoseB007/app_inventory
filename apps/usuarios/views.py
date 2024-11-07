from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse as HttpResponse
from django.db import transaction

from .models import Usuario
from .mixins import SuperUserRequiredMixin
from .forms import FormularioUsuario, FormularioPerfilUsuario
from .utils import generar_password, eliminar_acentos, enviar_email_usuario

from config import settings

import random
import string
import unicodedata
import json

# Create your views here.
class ListaUsuarios(SuperUserRequiredMixin, generic.ListView):
    model = Usuario
    template_name = "lista_usuarios.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de usuarios'
        context['entidad'] = 'Usuarios'
        context['crear_registro'] = reverse_lazy('usuarios:agregar-usuario')
        context['lista_registros'] = reverse_lazy('usuarios:lista-usuarios')
        return context
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        datos = []
        try:
            mostrar_datos = request.POST['mostrar_datos']
            if mostrar_datos == 'mostrar':
                for usuario in Usuario.objects.all():
                    datos.append(usuario.json_usuario())
            else:
                datos['error'] = 'Ha ocurrido un error'
        except Exception as e:
            datos['error'] = str(e)

        # return HttpResponse(empleados)
        return JsonResponse(datos, safe=False)


class CrearUsuario(SuperUserRequiredMixin, generic.CreateView):
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    success_url = reverse_lazy('usuarios:lista-usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un usuario'
        context['entidad'] = 'Usuarios'
        context['guardar_datos'] = 'guardar'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('usuarios:lista-usuarios')
        return context

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            guardar_datos = request.POST['guardar_datos']
            if guardar_datos == 'guardar':
                form = self.get_form()
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            first_name = form.cleaned_data['first_name'].split()
                            last_name = form.cleaned_data['last_name'].split()
                            
                            f_name = eliminar_acentos(first_name[0].lower())
                            l_name = eliminar_acentos(last_name[0].lower())

                            username_base = f"{f_name}_{l_name}"
                            
                            while True:
                                random_number = random.randint(0, 999)
                                username = f"{username_base}_{random_number}"
                                if not Usuario.objects.filter(username=username).exists():
                                    break
                            
                            password = generar_password(10)

                            usuario = form.save(commit=False)
                            usuario.username = username
                            usuario.set_password(password)

                            usuario.save()

                            for g in form.cleaned_data['groups']:
                                usuario.groups.add(g)

                            messages.success(request, 'El usuario se ha creado exitosamente.')
                            
                            # Acción que se ejecutará solo si la transacción se confirma  
                            transaction.on_commit(lambda: enviar_email_usuario(usuario, password))    
                    except Exception as e:
                        datos['error'] = str(e)
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)
    
    # Enviar correo electronico al usuario con sus credenciales de incio de sesión
    

class EditarUsuario(SuperUserRequiredMixin, generic.UpdateView):
    model = Usuario
    template_name = 'editar_usuario.html'
    form_class = FormularioUsuario
    success_url = reverse_lazy('usuarios:lista-usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar usuario'
        context['entidad'] = 'Usuarios'
        context['guardar_datos'] = 'editar'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('usuarios:lista-usuarios')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            guardar_datos = request.POST['guardar_datos']
            if guardar_datos == 'editar':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    messages.success(request, 'El registro se ha actualizado exitosamente.')
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)


class EliminarUsuario(SuperUserRequiredMixin, generic.DeleteView):
    model = Usuario
    template_name = 'eliminar_usuario.html'
    success_url = reverse_lazy('usuarios:lista-usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar usuario'
        context['entidad'] = 'Usuarios'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('usuarios:lista-usuarios')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            self.object.delete()
            messages.success(request, 'El registro se ha eliminado.')
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)



class EditarPerfilUsuario(generic.UpdateView):
    model = Usuario
    template_name = 'perfil.html'
    form_class = FormularioPerfilUsuario
    success_url = reverse_lazy('usuarios:lista-usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar perfil'
        context['entidad'] = 'Perfil'
        context['guardar_datos'] = 'editar'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('usuarios:perfil')
        return context

    def get_object(self, queryset = None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            accion = request.POST.get('guardar_datos')
            if accion == "editar":
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    messages.success(request, "Se ha actualizado el perfil exitosamente.")
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = "No ha ingresado a ninguna opción."
        except Exception as e:
            datos['error'] = str(e)

        return JsonResponse(datos)

