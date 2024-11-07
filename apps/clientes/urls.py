from django.urls import path

from apps.clientes.views import CrearCliente, ListaClientes, EditarCliente, EliminarCliente


app_name = "clientes"
urlpatterns = [
    path('', ListaClientes.as_view(), name="lista-clientes"),
    path('agregar-cliente/', CrearCliente.as_view(), name="agregar-cliente"),
    path('editar-cliente/<int:pk>/', EditarCliente.as_view(), name="editar-cliente"),
    path('eliminar-cliente/<int:pk>/', EliminarCliente.as_view(), name="eliminar-cliente"),
]
