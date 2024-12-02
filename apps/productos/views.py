from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import localtime, localdate
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum

from .models import Producto
from .forms import FormularioProducto #FormFiltroCategoria, FormRangoPrecio
from apps.usuarios.models import Usuario
from .mixins import ValidacionPermisosMixin
from apps.compras.models import OrdenDeCompra
from apps.ventas.models import OrdenDeVenta
from .utils import formatear_numero


from datetime import date


import json


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
        context['url_reedireccion'] = self.success_url
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


class DashboardView(LoginRequiredMixin, ValidacionPermisosMixin, generic.TemplateView):
    template_name = 'dashboard.html'
    permission_required = 'productos.view_dashboard'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Administración'
        context['entidad'] = 'Productos'
        context['lista_registros'] = reverse_lazy('productos:index')
        context['total_productos'] = self.total_productos()
        context['total_ordenes_compra'] = self.total_ordenes_compra_hoy()
        context['total_ordenes_venta'] = self.total_ordenes_venta_hoy()
        context['ultimos_productos_agregados'] = self.ultimos_productos_agregados()
        context['ultimas_compras'] = self.ultimas_compras_agregadas()
        context['total_meses_ordenes_venta_json'] = json.dumps(self.total_meses_ordenes_venta())
        context['total_sum_ventas_hoy'] = self.total_sum_ventas_hoy()
        context['total_sum_compras_hoy'] = self.total_sum_compras_hoy()
        context['productos_stock_insuficiente'] = self.productos_stock_insuficiente()
        return context
    
    def total_productos(self):
        total_productos = Producto.objects.all().count()
        return total_productos
    
    def total_ordenes_compra_hoy(self):
        hoy = localdate()
        ordenes_compra = OrdenDeCompra.objects.filter(fecha_de_orden__date=hoy).count()
        return ordenes_compra

    def total_ordenes_venta_hoy(self):
        hoy = localdate()
        ordenes_venta = OrdenDeVenta.objects.filter(fecha__date=hoy).count()
        return ordenes_venta
    
    def ultimos_productos_agregados(self):
        datos = []
        productos = Producto.objects.all().order_by('-id')[:3]
        for producto in productos:
            item = {
                'producto': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': formatear_numero(str(producto.precio))
            }
            datos.append(item)
        return datos

    def ultimas_compras_agregadas(self):
        datos = []
        compras = OrdenDeCompra.objects.all().order_by('-id')[:3]
        for c in compras:
            item = {
                'id': c.pk,
                'productos': [producto.producto.nombre for producto in c.detalledecompra_set.all()],
                'estado': c.estado,
                'fecha': c.fecha_de_orden.strftime("%d-%b-%Y"),
                'total': formatear_numero(str(c.total))
            }
            datos.append(item)
        return datos
    
    def total_meses_ordenes_venta(self):
        año = date.today().year
        lista_ordenes = []
        
        for mes in range(1, 13):
            total_ordenes = OrdenDeVenta.objects.filter(
                fecha__year=año,
                fecha__month=mes
            ).aggregate(total=Sum('total'))['total'] or 0
            
            lista_ordenes.append(float(total_ordenes))
        
        return lista_ordenes

    def total_sum_ventas_hoy(self):
        hoy = localdate()
        t_suma_ventas_hoy = OrdenDeVenta.objects.filter(fecha__date=hoy).aggregate(total=Sum('total'))['total'] or 0
        return formatear_numero(str(t_suma_ventas_hoy))
    
    def total_sum_compras_hoy(self):
        hoy = localdate()
        t_suma_compras_hoy = OrdenDeCompra.objects.filter(fecha_de_orden__date=hoy).aggregate(total=Sum('total'))['total'] or 0
        return formatear_numero(str(t_suma_compras_hoy))

    def productos_stock_insuficiente(self):
        prod = Producto.objects.filter(cantidad_en_stock__lte=10).order_by("cantidad_en_stock")[:4]

        lista_prod_stock_insuficiente = [
            {'nombre': p.nombre, 'stock': p.cantidad_en_stock} for p in prod
        ]

        if not lista_prod_stock_insuficiente:
            return None

        return lista_prod_stock_insuficiente


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

