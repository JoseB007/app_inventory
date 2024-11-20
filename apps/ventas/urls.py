from django.urls import path
from apps.ventas import views


app_name = 'ventas'
urlpatterns = [
    path('', views.ListaVentas.as_view(), name='lista-ventas'),
    path('agregar-venta/', views.CrearVenta.as_view(), name='agregar-venta'),
    path('reportes/facturas/<int:pk>/', views.GenerarReportePDF.as_view(), name='reportes_factura_venta'),
]