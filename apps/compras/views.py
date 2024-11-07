from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.productos.models import Producto
from .mixins import ValidacionPermisosMixin
from apps.compras.forms import FormularioOrdenDeCompra #FormularioProducto, FormularioAutoCompleteProducto
from apps.compras.models import OrdenDeCompra, DetalleDeCompra

import json

# Create your views here.
class ListaCompras(ValidacionPermisosMixin, generic.ListView):
    model = OrdenDeCompra
    template_name = 'lista_compras.html'
    permission_required = ('compras.view_ordendecompra', 'compras.view_detalledecompra')
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            mostrar_datos = self.request.POST['mostrar_datos']
            if mostrar_datos == 'mostrar':
                datos = []
                for orden in OrdenDeCompra.objects.all():
                    datos.append(orden.orden_json())
            elif mostrar_datos == 'detalle':
                datos = []
                for i in DetalleDeCompra.objects.filter(orden_de_compra_id=request.POST['id']):
                    datos.append(i.detalle_json())
            else:
                datos['error'] = 'Ha ocurrido un error al intentar mostrar los datos'
        except Exception as e:
            datos['error'] = str(e)
        
        # print(f'Detalle de la compra: {datos}')
        return JsonResponse(datos, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ordenes de Compra'
        context['entidad'] = 'Ordenes de Compra'
        context['crear_registro'] = reverse_lazy('compras:agregar-compra')
        context['lista_registros'] = reverse_lazy('compras:lista-compras')
        return context
    

class CrearOrdenDeCompra(ValidacionPermisosMixin, generic.CreateView):
    model = OrdenDeCompra
    form_class = FormularioOrdenDeCompra
    template_name = 'crear_compra.html'
    success_url = reverse_lazy('compras:lista-compras')
    permission_required = ('compras.view_ordendecompra', 'compras.view_detalledecompra', 'compras.add_ordendecompra', 'compras.add_detalledecompra')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar nueva compra'
        context['entidad'] = 'Ordenes de Compra'
        context['guardar_datos'] = 'guardar'
        context['url_reedireccion'] = self.success_url
        context['lista_registros'] = reverse_lazy('compras:lista-compras')
        #context['form_producto'] = FormularioProducto()
        #context['form_autocomplete'] = FormularioAutoCompleteProducto()
        return context
 
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            mostrar_datos = self.request.POST['accion']
            if mostrar_datos == 'buscar':
                datos = []
                productos = Producto.objects.filter(nombre__icontains=self.request.POST['term'])[0:9]
                for i in productos:
                    item = {}
                    item['id'] = i.id
                    item['nombre'] = i.nombre
                    item['descripcion'] = i.descripcion
                    item['precio'] = i.precio
                    # Agregar la clave 'value' para mostrar los datos en el componente HTML
                    item['value'] = i.nombre
                    datos.append(item)
            elif mostrar_datos == 'guardar':
                compra = json.loads(self.request.POST['compra'])
                
                orden_compra = OrdenDeCompra(
                    proveedor_id = compra['proveedor'],
                    estado = compra['estado'],
                    subtotal = float(compra['subtotal']),
                    iva = float(compra['iva']),
                    total = float(compra['total']),
                )
                orden_compra.save()

                for i in compra['productos']:
                    detalle_compra = DetalleDeCompra(
                        orden_de_compra_id = orden_compra.id,
                        producto_id = i['id'],
                        precio_unitario = float(i['precio']),
                        cantidad = int(i['cantidad']),
                        subtotal = float(i['subtotal']),
                    )
                    detalle_compra.save()

                    producto = get_object_or_404(Producto, pk=detalle_compra.producto.id)
                    producto.cantidad_en_stock += detalle_compra.cantidad
                    producto.save()
                
                if orden_compra and detalle_compra:
                    messages.success(request, 'Se ha añadido una nueva compra y productos al inventario.')
            else:
                datos['error'] = 'Ha ocurrido un error al intentar mostrar los datos'
        except Exception as e:
            datos['error'] = str(e)

        return JsonResponse(datos, safe=False)
