from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from apps.clientes.models import Cliente
from apps.clientes.forms import FormularioCliente
from apps.clientes.mixins import ValidacionPermisosMixin

# Create your views here.


class ListaClientes(ValidacionPermisosMixin, ListView):
    model = Cliente
    template_name = 'lista_clientes.html'
    permission_required = 'clientes.view_cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de clientes'
        context['entidad'] = 'Clientes'
        context['lista_registros'] = reverse_lazy('clientes:lista-clientes')
        context['crear_registro'] = reverse_lazy('clientes:agregar-cliente')
        return context

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = self.request.POST['action']
            if action == 'list_data':
                data = []
                # Lista de clientes excepto el cliente '0000000000'
                for cliente in Cliente.objects.exclude(documento_identidad='0000000000'):
                    data.append(cliente.jsonCliente())
            else:
                data['error'] = 'No se ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


class CrearCliente(ValidacionPermisosMixin, CreateView):
    model = Cliente
    form_class = FormularioCliente
    template_name = 'crear_cliente.html'
    success_url = reverse_lazy('clientes:lista-clientes')
    permission_required = 'clientes.add_cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar cliente'
        context['entidad'] = 'Clientes'
        context['guardar_datos'] = 'guardar'
        context['lista_registros'] = reverse_lazy('clientes:lista-clientes')
        context['url_reedireccion'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            accion = self.request.POST['guardar_datos']
            msj = self.request.POST.get('msj')
            if accion == "guardar":
                form = self.get_form()
                if form.is_valid():
                    cliente = form.save()
                    datos['cliente'] = {
                        'id': cliente.id,
                        'nombre': cliente.nombre,
                        'documento_identidad': cliente.documento_identidad,
                        'telefono': cliente.telefono,
                        'email': cliente.correo_electronico,
                        'direccion': cliente.direccion,
                    }
                    if msj != 'no_msj':
                        messages.success(request, 'El registro se ha creado exitosamente.')
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            datos['error'] = str(e)
    
        return JsonResponse(datos)
    

class EditarCliente(ValidacionPermisosMixin, UpdateView):
    model = Cliente
    template_name = 'editar_cliente.html'
    form_class = FormularioCliente
    success_url = reverse_lazy('clientes:lista-clientes')
    permission_required = 'clientes.change_cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cliente'
        context['entidad'] = 'Clientes'
        context['guardar_datos'] = 'editar'
        context['lista_registros'] = reverse_lazy('clientes:lista-clientes')
        context['url_reedireccion'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.documento_identidad != '0000000000':
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            accion = self.request.POST.get('guardar_datos')
            if accion == 'editar':
                form = self.get_form()
                if form.is_valid():
                    cliente = form.save(commit=False)
                    if cliente.pk == 1:
                        datos['error'] = 'Este registro no puede editarse.'
                    else:
                        cliente.save()
                        messages.success(request, 'El registro se ha actualizado exitosamente.')
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No se ha ingresado ninguna opción'
        except Exception as e:
            datos['error'] = str(e)

        return JsonResponse(datos)


class EliminarCliente(ValidacionPermisosMixin, DeleteView):
    model = Cliente
    template_name = 'eliminar_cliente.html'
    success_url = reverse_lazy('clientes:lista-clientes')
    permission_required = 'clientes.delete_cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cliente'
        context['entidad'] = 'Clientes'
        context['lista_registros'] = reverse_lazy('clientes:lista-clientes')
        context['url_reedireccion'] = self.success_url
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

