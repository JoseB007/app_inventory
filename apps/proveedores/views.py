# from typing import Any
# from django.http import HttpRequest
# from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Proveedor
from .forms import FormularioProveedor
from .mixins import SuperUserRequiredMixin, ValidacionPermisosMixin

# Create your views here.
class ListaProveedores(ValidacionPermisosMixin, generic.ListView):
    model = Proveedor
    template_name = 'lista_proveedores.html'
    permission_required = 'proveedores.view_proveedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de proveedores'
        context['entidad'] = 'Proveedores'
        context['lista_registros'] = reverse_lazy('proveedores:lista-proveedores')
        context['crear_registro'] = reverse_lazy('proveedores:crear-proveedor')
        return context

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            mostrar_datos = self.request.POST['mostrar_datos']
            if mostrar_datos == 'mostrar':
                datos = []
                for proveedor in Proveedor.objects.all():
                    datos.append(proveedor.json_Proveedor())
            else:
                datos['error'] = 'Hubo un error al tratar de mostrar los datos'
        except  Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos, safe=False)


class CrearProveedor(ValidacionPermisosMixin, generic.CreateView):
    model = Proveedor
    template_name = 'crear_proveedor.html'
    form_class = FormularioProveedor
    success_url = reverse_lazy('proveedores:lista-proveedores')
    permission_required = 'proveedores.add_proveedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar proveedor'
        context['entidad'] = 'Proveedores'
        context['lista_registros'] = reverse_lazy('proveedores:lista-proveedores')
        context['url_reedireccion'] = self.success_url
        context['guardar_datos'] = 'guardar'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            accion = request.POST['guardar_datos']
            if accion == 'guardar':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    print(form.cleaned_data)
                    messages.success(request, 'El registro se ha creado exitosamente.')
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)


class EliminarProveedor(ValidacionPermisosMixin, generic.DeleteView):
    model = Proveedor
    template_name = 'eliminar_proveedor.html'
    success_url = reverse_lazy('proveedores:lista-proveedores')
    permission_required = 'proveedores.delete_proveedor'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar proveedor'
        context['entidad'] = 'Proveedores'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('proveedores:lista-proveedores')
        return context
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            self.object.delete()
            messages.success(request, 'El registro se ha eliminado.')
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)
    

class EditarProveedor(ValidacionPermisosMixin, generic.UpdateView):
    model = Proveedor
    template_name = 'editar_proveedor.html'
    form_class = FormularioProveedor
    success_url = reverse_lazy('proveedores:lista-proveedores')
    permission_required = 'proveedores.change_proveedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar proveedor'
        context['entidad'] = 'Proveedores'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('proveedores:lista-proveedores')
        context['guardar_datos'] = 'editar'
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


