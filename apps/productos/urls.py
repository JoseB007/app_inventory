from django.urls import path
from . import views

app_name = 'productos'
urlpatterns = [
    path('', views.ListaProductos.as_view(), name='index'),
    path('detalle-producto/<int:pk>/', views.DetalleProducto.as_view(), name='detalle-producto'),
    path('agregar-producto/', views.CrearProducto.as_view(), name='crear-producto'),
    path('editar-producto/<int:pk>/', views.ActualizarProducto.as_view(), name='editar-producto'),
    path('eliminar-producto/<int:pk>/', views.EliminarProducto.as_view(), name='eliminar-producto'),
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # Historial
    path('historial/', views.HistorialProducto.as_view(), name='historial')
]