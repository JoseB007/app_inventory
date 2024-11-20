from django.urls import path


from apps.inventario import views


app_name = 'mov_inventory'
urlpatterns = [
    path('', views.ListaMovimientosIventario.as_view(), name='movimientos'),
]