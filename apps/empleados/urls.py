from django.urls import path
from . import views

app_name = 'empleados'
urlpatterns = [
    path('', views.ListaEmpleados.as_view(), name='lista-empleados'),
    path('agregar-empleado/', views.CrearEmpleado.as_view(), name='agregar-empleado'),
    path('editar-empleado/<int:pk>/', views.EditarEmpleado.as_view(), name='editar-empleado'),
    path('eliminar-empleado/<int:pk>/', views.EliminarEmpleado.as_view(), name='eliminar-empleado'),
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]