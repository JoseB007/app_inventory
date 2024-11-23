from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.contrib.auth.mixins import LoginRequiredMixin


from apps.inventario.models import MovimientoInventario
from apps.inventario.mixins import ValidacionPermisosMixin
from apps.empleados.models import Empleado

# Create your views here.
class ListaMovimientosIventario(LoginRequiredMixin, ValidacionPermisosMixin, ListView):
    model = MovimientoInventario
    template_name = "mov_inventario.html"
    permission_required = 'inventario.view_movimientoinventario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entidad'] = 'Movimientos de Inventario'
        context['title'] = 'Movimientos de Inventario'
        context['history'] = reverse_lazy('productos:historial')
        context['lista_registros'] = reverse_lazy('mov_inventory:movimientos')
        #context['crear_registro'] = reverse_lazy('productos:crear-producto')
        return context
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            accion = request.POST.get('accion')

            if accion == 'mostrar':
                datos = []
                for i in MovimientoInventario.objects.all():
                    datos.append(i.json_mov_inventario())
            elif accion == 'detalle':
                datos = []
                lista_ord_ventas = []
                lista_ord_compra = []
                mov_inv = get_object_or_404(MovimientoInventario, pk=request.POST.get('id'))
                for orden_venta in mov_inv.ordenes_venta.all():
                    item = {
                        'id': orden_venta.id,
                        'estado': orden_venta.estado,
                        'total': orden_venta.total,
                    }
                    item['fecha'] = localtime(orden_venta.fecha).strftime('%d de %b de %Y a las %H:%M')
                    item['empleado'] = str(orden_venta.empleado) if orden_venta.empleado else None,
                    lista_ord_ventas.append(item)
                for orden_compra in mov_inv.ordenes_compra.all():
                    item = {
                        'id': orden_compra.id,
                        'estado': orden_compra.estado,
                        'total': orden_compra.total,
                    }
                    item['fecha'] = localtime(orden_compra.fecha_de_orden).strftime('%d de %b de %Y a las %H:%M')
                    item['empleado'] = str(orden_compra.empleado) if orden_compra.empleado else None,
                    lista_ord_compra.append(item)
                datos.append(lista_ord_ventas)
                datos.append(lista_ord_compra)
            else:
                datos['error'] = 'Ha ocurrido un error'
        except Exception as e:
            datos['error'] = str(e)

        # print(datos)
        return JsonResponse(datos, safe=False)

