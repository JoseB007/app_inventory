from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.ListaUsuarios.as_view(), name='lista-usuarios'),
    path('agregar-usuario/', views.CrearUsuario.as_view(), name='agregar-usuario'),
    path('editar-usuario/<int:pk>/', views.EditarUsuario.as_view(), name='editar-usuario'),
    path('eliminar-usuario/<int:pk>/', views.EliminarUsuario.as_view(), name='eliminar-usuario'),
    path('perfil/', views.EditarPerfilUsuario.as_view(), name='perfil'),
]