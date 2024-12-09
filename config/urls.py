"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('apps.productos.urls')),
    path('login/', include('apps.login.urls')),
    path('empleados/', include('apps.empleados.urls')),
    path('proveedores/', include('apps.proveedores.urls')),
    path('compras/', include('apps.compras.urls')),
    path('ventas/', include('apps.ventas.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('movimientos-inventario/', include('apps.inventario.urls')),
    path('configuracion/', include('apps.configuracion.urls')),
    path('', RedirectView.as_view(url='/productos/dashboard/', permanent=True)),
]
