from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.http import JsonResponse
from django.contrib import messages


from apps.configuracion.models import Configuracion
from apps.configuracion.forms import FormConfig


# Create your views here.
class Configurar(CreateView):
    model = Configuracion
    template_name = "config.html"
    form_class = FormConfig
    success_url = reverse_lazy('productos:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Configuración"
        context['entidad'] = 'Dashboard'
        context['lista_registros'] = reverse_lazy('productos:dashboard')
        context['url_redireccion'] = self.success_url
        context['action'] = 'guardar'
        return context
    
    def post(self, request, *args, **kwargs):
        datos = {}
        action = request.POST.get('action')
        if action == 'guardar':
            try:
                form = self.get_form()
                if form.is_valid():
                    print(form.cleaned_data)
                    config_empresa = Configuracion.objects.first()
                    if config_empresa:
                        config_empresa.nombre_empresa = form.cleaned_data['nombre_empresa']
                        config_empresa.nit = form.cleaned_data['nit']
                        config_empresa.email = form.cleaned_data['email']
                        config_empresa.telefono = form.cleaned_data['telefono']
                        config_empresa.save()
                    else:
                        form.save()
                    messages.success(request, "Se han aplicado las configuraciones correctamente.")
                else:
                    datos['error'] = form.errors
            except Exception as e:
                datos['error'] = str(e)
        else:
            datos['error'] = 'Existió un error al mostrar los datos'
        return JsonResponse(datos)
