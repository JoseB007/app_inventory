from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Producto
from .forms import FormularioProducto #FormFiltroCategoria, FormRangoPrecio
from apps.usuarios.models import Usuario
from .mixins import ValidacionPermisosMixin, SuperuserRequiredMixin


class ListaProductos(LoginRequiredMixin, ValidacionPermisosMixin, generic.ListView):
    model = Producto
    template_name = 'lista_productos.html'
    context_object_name = 'lista_productos'
    permission_required = 'productos.view_producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entidad'] = 'Productos'
        context['title'] = 'Lista de productos'
        context['history'] = reverse_lazy('productos:historial')
        context['lista_registros'] = reverse_lazy('productos:index')
        context['crear_registro'] = reverse_lazy('productos:crear-producto')
        # context['FormFiltroCategoria'] = FormFiltroCategoria()
        # context['FormRangoPrecio'] = FormRangoPrecio()
        return context
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = []
        try:
            mostrar_datos = request.POST['mostrar_datos']
            if mostrar_datos == 'mostrar':
                for producto in Producto.objects.all():
                    datos.append(producto.json_producto())
            else:
                datos['error'] = 'Ha ocurrido un error'
        except Exception as e:
            datos['error'] = str(e)

        return JsonResponse(datos, safe=False)
    

class CrearProducto(LoginRequiredMixin, ValidacionPermisosMixin, generic.CreateView):
    model = Producto
    template_name = 'crear_producto.html'
    form_class = FormularioProducto
    success_url = reverse_lazy('productos:index') # Construir una url
    permission_required = 'productos.add_producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar producto'
        context['entidad'] = 'Productos'
        context['lista_registros'] = reverse_lazy('productos:index')
        context['url_reedireccion'] = reverse_lazy('productos:index')
        context['guardar_datos'] = 'guardar'
        return context
    
    def post(self, request, *args, **kwargs):   
        datos = {}     
        try:
            guardar_datos = request.POST['guardar_datos']
            if guardar_datos == 'guardar':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    messages.success(request, 'El registro se ha creado exitosamente.')
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)
    
        # form = self.get_form()
        # if form.is_valid():
        #     form.save()
        #     return redirect(self.success_url) # Redirigir a una url
        # # En caso de que el formulario no sea valido, se envía la información nuevamente a la plantilla del formulario
        # return render(request, self.template_name, {'form': form})
         

class ActualizarProducto(LoginRequiredMixin, ValidacionPermisosMixin, generic.UpdateView):
    model = Producto
    template_name = 'crear_producto.html'
    form_class = FormularioProducto
    success_url = reverse_lazy('productos:index')
    permission_required = 'productos.change_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar producto'
        context['entidad'] = 'Productos'
        context['lista_registros'] = reverse_lazy('productos:index')
        context['url_reedireccion'] = self.success_url
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


class EliminarProducto(LoginRequiredMixin, ValidacionPermisosMixin, generic.DeleteView):
    model = Producto
    template_name = 'eliminar_producto.html'
    success_url = reverse_lazy('productos:index')
    permission_required = 'productos.delete_producto'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar producto'
        context['entidad'] = 'Productos'
        context['lista_registros'] = reverse_lazy('productos:index')
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


class DetalleProducto(generic.DetailView):
    model = Producto
    template_name = 'detalle_producto.html'
    context_object_name = 'detalle_producto'


class DashboardView(generic.TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Administración'
        context['entidad'] = 'Productos'
        context['lista_registros'] = reverse_lazy('productos:index')
        return context


class HistorialProducto(LoginRequiredMixin, generic.TemplateView):
    template_name = 'historial_producto.html'

    def get(self, request, *args, **kwargs):
        datos = []
        queryset = Producto.historial.all()
        for p in queryset:
            usuario = Usuario.objects.get(id=p.history_user_id)
            item = {
                'id': p.id,
                'nombre': p.nombre,
                'precio': p.precio,
                'stock': p.cantidad_en_stock,
                'fecha_historial': p.history_date,
                'tipo': p.history_type,
                'empleado': usuario.get_full_name() if usuario.first_name else usuario.username,
            }
            datos.append(item)
        context = self.get_context_data(**kwargs)
        context['datos'] = datos
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de cambios'
        context['entidad'] = 'Productos'
        context['lista_registros'] = reverse_lazy('productos:index')
        context['history'] = reverse_lazy('productos:historial')
        return context

