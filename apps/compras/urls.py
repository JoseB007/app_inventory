from django.urls import path

from apps.compras import views

app_name = 'compras'
urlpatterns = [
    path('', views.ListaCompras.as_view(), name='lista-compras'),
    path('agregar-compra/', views.CrearOrdenDeCompra.as_view(), name='agregar-compra'),
    
]