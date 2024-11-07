from django.urls import path
from . import views

app_name = 'proveedores'
urlpatterns = [
    path('', views.ListaProveedores.as_view(), name='lista-proveedores'),
    path('agregar-proveedor', views.CrearProveedor.as_view(), name='crear-proveedor'),
    path('eliminar-proveedor/<int:pk>/', views.EliminarProveedor.as_view(), name='eliminar-proveedor'),
    path('editar-proveedor/<int:pk>/', views.EditarProveedor.as_view(), name='editar-proveedor'),
]