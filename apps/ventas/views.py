import json

from typing import Any

from django.views import generic
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.timezone import localdate
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.productos.models import Producto

from apps.ventas.utils import formatear_numero, formatear_fecha_hora_inicio, formatear_fecha_hora_fin
from apps.ventas.forms import FormularioOrdenDeVenta, FormularioFiltros
from apps.ventas.mixins import ValidacionPermisosMixin
from apps.ventas.models import OrdenDeVenta, DetalleOrdenDeVenta

from apps.clientes.forms import FormularioCliente
from apps.clientes.models import Cliente

from apps.inventario.models import MovimientoInventario

from apps.empleados.models import Empleado

from xhtml2pdf import pisa


# Create your views here.
class ListaVentas(LoginRequiredMixin, ValidacionPermisosMixin, generic.ListView):
    model = OrdenDeVenta
    template_name = 'lista_ventas.html'
    permission_required = ("ventas.view_ordendeventa", "ventas.view_detalleordendeventa")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ventas'
        context['entidad'] = 'Ordenes de Ventas'
        context['lista_registros'] = reverse_lazy('ventas:lista-ventas')
        context['crear_registro'] = reverse_lazy('ventas:agregar-venta')
        context['formularioFiltros'] = FormularioFiltros()
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
            elif action == "filtrar":
                campos_filtros = json.loads(request.POST.get('filtros'))
            
                id_cliente = campos_filtros[0]['value']
                f_ini_str = campos_filtros[1]['value']
                f_end_str = campos_filtros[2]['value']
                estado_venta = campos_filtros[3]['value']

                if not estado_venta:
                    estado_venta = OrdenDeVenta.ESTADO_DE_ORDEN[1]

                if not id_cliente:
                    data['error'] = "Ningún cliente seleccionado."
                else:
                    data=[]
                    fecha_ini = formatear_fecha_hora_inicio(f_ini_str)
                    fecha_fin = formatear_fecha_hora_fin(f_end_str)

                    if fecha_fin > fecha_ini:
                        orden_filtrada = OrdenDeVenta.objects.filter(cliente=int(id_cliente), fecha__range=(fecha_ini, fecha_fin), estado=estado_venta)

                        for ord_filt in orden_filtrada:
                            data.append(ord_filt.orden_Json())
            else:
                data['error'] = 'No se ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class CrearVenta(LoginRequiredMixin, ValidacionPermisosMixin, generic.CreateView):
    model = OrdenDeVenta
    form_class = FormularioOrdenDeVenta
    template_name = 'crear_venta.html'
    success_url = reverse_lazy('productos:dashboard')
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
        # Obtener los ID de los usuarios relacionados con la tabla EMPLEADOS
        empleados = Empleado.objects.values_list('usuario', flat=True)
        # Validar si el ID del usuario en sesión se encuentra relacionado con la tabla EMPLEADOS
        if request.user.pk not in empleados:
            messages.info(request, "La sesión actual no tiene relación con ningún empleado.")
            return redirect(self.success_url)
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

                        # Lista para almacenar errores
                        data_error = []

                        # Verificar disponibilidad de stock para todos los productos antes de crear la orden de venta
                        for venta_producto in venta['productos']:
                            producto = get_object_or_404(Producto, id=venta_producto['id'])
                            
                            if venta_producto['cantidad'] > producto.cantidad_en_stock:
                                data_error.append(f'El stock de "{venta_producto["label"]}" es insuficiente para realizar esta venta.')

                        # Si hay errores de stock, cancelar la transacción
                        if len(data_error) > 0:
                            data['error'] = data_error
                            raise ValueError(data_error) # Forzar rollback
                        
                        # Si no hay errores de stock se procede a crear la orden de venta juntos con los detalles de la venta
                        # Obtener empleado
                        empleado = Empleado.objects.get(usuario=request.user.pk)

                        # Crear la orden de venta
                        orden_venta = OrdenDeVenta(
                            empleado_id=empleado.pk,
                            cliente_id=int(venta['cliente']),
                            estado=venta['estado'],
                            subtotal=float(venta['subtotal']),
                            iva=float(venta['iva']),
                            total=float(venta['total']),
                        )
                        orden_venta.save()

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
                        
                        # Crear un movimiento de inventario para todas las ventas que se realicen en el dia. Establecer el día del movimiento que será obtenido o creado 
                        hoy = localdate()
                        # Obtener el movimiento en caso de que exista, con la fecha de el día o crear uno nuevo
                        movimiento, creado = MovimientoInventario.objects.get_or_create(fecha=hoy)

                        if movimiento or creado:
                            # Asocia las órdenes de hoy
                            ordenes_venta_hoy = OrdenDeVenta.objects.filter(fecha__date=hoy)
                            movimiento.ordenes_venta.set(ordenes_venta_hoy)

                            # Actualiza los totales
                            movimiento.actualizar_totales()

                            # Mensaje de éxito para la creación de la orden de venta
                            messages.success(request, 'Nueva orden de venta registrada.')
                        else:
                            data_error.append(f"El movimiento de inventario con fecha {hoy} no existe")
                            data['error'] = data_error
                            raise ValueError(data_error)
                except Exception as e:
                    data['error'] = e.args[0]
            else:
                data['error'] = 'No se ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


class GenerarReportePDF(LoginRequiredMixin, ValidacionPermisosMixin, generic.View):
    permission_required = ("ventas.view_ordendeventa", "ventas.view_detalleordendeventa", "ventas.add_ordendeventa", "ventas.add_detalleordendeventa")
    
    def get(request, self, *args, **kwargs):
        orden = OrdenDeVenta.objects.get(pk=kwargs.get('pk'))
        detalle = orden.detalleordendeventa_set.all()

        subtotal = orden.subtotal
        iva = orden.iva
        total = orden.total

        orden.subtotal = formatear_numero(str(subtotal))
        orden.iva = formatear_numero(str(iva))
        orden.total = formatear_numero(str(total))

        context = {
            'orden': orden,
            'datos_empresa': {
                'nombre': 'System Hight',
                'NIT': '9999999999',
                'direccion': 'Pasto-Nariño',
            }
        }
        html = render_to_string('reporte_factura.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="archivo.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar PDF', status=400)
        return response

