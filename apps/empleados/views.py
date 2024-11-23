from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Empleado
from .forms import FormularioEmpleado
from .mixins import SuperuserRequiredMixin


# Create your views here.
class CrearEmpleado(LoginRequiredMixin, SuperuserRequiredMixin, generic.CreateView):
    model = Empleado
    form_class = FormularioEmpleado
    template_name = 'crear_empleado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un empleado'
        context['entidad'] = 'Empleados'
        context['guardar_datos'] = 'guardar'
        context['url_reedireccion'] = reverse_lazy('empleados:lista-empleados')
        context['lista_registros'] = reverse_lazy('empleados:lista-empleados')
        return context

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            guardar_datos = request.POST['guardar_datos']
            if guardar_datos == 'guardar':
                form = self.get_form()
                if form.is_valid():
                    messages.success(request, 'El registro se ha creado exitosamente.')
                    form.save()
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)


class ListaEmpleados(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    model = Empleado
    template_name = 'lista_empleados.html'
    context_object_name = 'lista_empleados'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de empleados'
        context['entidad'] = 'Empleados'
        context['crear_registro'] = reverse_lazy('empleados:agregar-empleado')
        context['lista_registros'] = reverse_lazy('empleados:lista-empleados')
        return context
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        datos = []
        try:
            mostrar_datos = request.POST['mostrar_datos']
            if mostrar_datos == 'mostrar':
                for empleado in Empleado.objects.all():
                    datos.append(empleado.empleado_to_json())
            else:
                datos['error'] = 'Ha ocurrido un error'
        except Exception as e:
            datos['error'] = str(e)

        # return HttpResponse(empleados)
        return JsonResponse(datos, safe=False)


class EditarEmpleado(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    model = Empleado
    template_name = 'crear_empleado.html'
    form_class = FormularioEmpleado
    success_url = reverse_lazy('empleados:lista-empleados')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Empleado'
        context['entidad'] = 'Empleados'
        context['lista_registros'] = reverse_lazy('empleados:lista-empleados')
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
                    messages.success(request, 'El registro se ha actualizado exitosamente.')
                    form.save()
                else:
                    datos['error'] = form.errors
            else:
                datos['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            datos['error'] = str(e)
        
        return JsonResponse(datos)


class EliminarEmpleado(LoginRequiredMixin, SuperuserRequiredMixin, generic.DeleteView):
    model = Empleado
    template_name = 'eliminar_empleado.html'
    success_url = reverse_lazy('empleados:lista-empleados')

    def dispatch(self, request, *args, **kwargs):
        self.objetc = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Empleado'
        context['entidad'] = 'Empleados'
        context['lista_registros'] = reverse_lazy('empleados:lista-empleados')
        context['url_reedireccion'] = self.success_url
        return context
    
    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            self.objetc.delete()
            messages.success(request, 'El registro se ha eliminado.')
        except Exception as e:
            datos['error'] = str(e)

        return JsonResponse(datos)


class DashboardView(LoginRequiredMixin, SuperuserRequiredMixin, generic.TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Administración'
        return context



