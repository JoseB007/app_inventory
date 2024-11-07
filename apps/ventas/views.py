import json

from typing import Any

from django.views import generic
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse


from apps.productos.models import Producto
from apps.clientes.forms import FormularioCliente
from apps.ventas.forms import FormularioOrdenDeVenta
from apps.ventas.mixins import ValidacionPermisosMixin
from apps.ventas.models import OrdenDeVenta, DetalleOrdenDeVenta


# Create your views here.
class ListaVentas(ValidacionPermisosMixin, generic.ListView):
    model = OrdenDeVenta
    template_name = 'lista_ventas.html'
    permission_required = ("ventas.view_ordendeventa", "ventas.view_detalleordendeventa")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ventas'
        context['entidad'] = 'Ordenes de Ventas'
        context['lista_registros'] = reverse_lazy('ventas:lista-ventas')
        context['crear_registro'] = reverse_lazy('ventas:agregar-venta')
        return context

    @csrf_exempt
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = self.request.POST['action']
            if action == 'list_data':
                data = []
                for venta in OrdenDeVenta.objects.all():
                    data.append(venta.orden_Json())
            elif action == 'detail':
                data = []
                for i in DetalleOrdenDeVenta.objects.filter(orden_de_venta_id=self.request.POST['id']):
                    data.append(i.json_detalle_venta())
            else:
                data['error'] = 'No se ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


class CrearVenta(ValidacionPermisosMixin, generic.CreateView):
    model = OrdenDeVenta
    form_class = FormularioOrdenDeVenta
    template_name = 'crear_venta.html'
    success_url = reverse_lazy('ventas:lista-ventas')
    permission_required = ("ventas.view_ordendeventa", "ventas.view_detalleordendeventa", "ventas.add_ordendeventa", "ventas.add_detalleordendeventa")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar nueva venta'
        context['entidad'] = 'Ordenes de Ventas'
        context['guardar_datos'] = 'guardar'
        context['msj'] = 'no_msj'
        context['lista_registros'] = reverse_lazy('ventas:lista-ventas')
        context['url_redireccion'] = self.success_url
        context['formCliente'] = FormularioCliente()
        return context

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar':
                data = []
                productos = Producto.objects.filter(
                    nombre__icontains=request.POST['term'])[0:9]
                for producto in productos:
                    item = {}
                    if producto.cantidad_en_stock > 0:
                        item['id'] = producto.id
                        # Agregar la llave 'label o value' para la visualización de los datos en el complemento
                        item['value'] = producto.nombre
                        item['precio'] = producto.precio
                        data.append(item)
            elif action == 'guardar':
                try:
                    with transaction.atomic():
                        venta = json.loads(request.POST['sale'])
                        
                        # Crear la orden de venta
                        orden_venta = OrdenDeVenta(
                            cliente_id=int(venta['cliente']),
                            estado=venta['estado'],
                            subtotal=float(venta['subtotal']),
                            iva=float(venta['iva']),
                            total=float(venta['total']),
                        )
                        orden_venta.save()

                        # Lista para almacenar errores
                        data_error = []

                        # Verificar disponibilidad de stock para todos los productos
                        for venta_producto in venta['productos']:
                            producto = get_object_or_404(Producto, id=venta_producto['id'])
                            
                            if venta_producto['cantidad'] > producto.cantidad_en_stock:
                                data_error.append(f'El stock de "{venta_producto["label"]}" es insuficiente para realizar esta venta.')

                        # Si hay errores de stock, cancelar la transacción
                        if len(data_error) > 0:
                            data['error'] = data_error
                            raise ValueError(data_error) # Forzar rollback

                        # Crear los detalles de la orden de venta
                        for venta_producto in venta['productos']:
                            producto = get_object_or_404(Producto, id=venta_producto['id'])
                            
                            detalle_venta = DetalleOrdenDeVenta(
                                orden_de_venta_id=orden_venta.pk,
                                producto_id=producto.pk,
                                cantidad=int(venta_producto['cantidad']),
                                precio_unitario=producto.precio, 
                            )
                            detalle_venta.subtotal = detalle_venta.cantidad * detalle_venta.precio_unitario
                            detalle_venta.save()

                            # Actualizar el stock del producto
                            producto.cantidad_en_stock -= detalle_venta.cantidad
                            
                            producto.save()
                        messages.success(request, 'Nueva orden de venta registrada.')
                except Exception as e:
                    data['error'] = e.args[0]
            else:
                data['error'] = 'No se ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


class GenerarReportePDF(generic.View):

    pass

